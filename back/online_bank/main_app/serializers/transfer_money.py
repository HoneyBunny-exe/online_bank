from rest_framework import serializers
from rest_framework import exceptions
from main_app.models import TFA, Account, Card, Contract, Operation
from .TFA import TwoFactoryAuthentication
import logging
from utils import custom_validators
from django.db import transaction, models
from utils import UserContext, CurrencyConverter
from decimal import Decimal


def check_balance(account: Account, amount_money):
    if account.type_account == Account.TypeAccount.DEBIT:
        if account.balance < amount_money:
            return False

    elif account.type_account == Account.TypeAccount.CREDIT:
        contract = Contract.objects.get(account=account)
        credit_limit = Decimal(contract.description["max_debt_amount"])
        if credit_limit + account.balance < amount_money:
            return False

    return True


class CreateTransferMoneySerializer(serializers.Serializer):
    account_send = serializers.CharField()
    token_card_send = serializers.CharField(required=False)
    account_recv = serializers.CharField(required=False)
    card_number_recv = serializers.CharField(required=False)
    amount_money = serializers.DecimalField(min_value=0, max_digits=32, decimal_places=2)
    description = serializers.CharField(required=False
                                        )
    _response = None

    def validate_account_recv(self, account_number):
        custom_validators.validate_account_number(account_number, is_api=True)
        return account_number

    def validate_card_number_recv(self, card_number):
        custom_validators.validate_card_number(card_number, is_api=True)
        return card_number

    def validate_account_send(self, account_send):
        custom_validators.validate_account_number(account_send, is_api=True)
        return account_send

    def validate(self, attrs):
        account_recv = attrs.get("account_recv", None)
        card_number_recv = attrs.get("card_number_recv", None)
        if not (account_recv or card_number_recv) or account_recv and card_number_recv:
            raise exceptions.ValidationError("Необходимо указать либо номер счета, либо карту получателя")

        return attrs

    def create(self, validated_data):
        user = UserContext.get_user()
        account_recv = validated_data.get("account_recv", None)
        card_number_recv = validated_data.get("card_number_recv", None)
        token_card_send = validated_data.get("token_card_send", None)
        about = validated_data.get("description", None)

        account_send = validated_data["account_send"]
        amount_money: Decimal = validated_data["amount_money"]

        try:
            account_send_obj = Account.objects.get(account_number=account_send, user=user)
            if token_card_send is not None:
                card_send_obj = Card.objects.get(token_card=token_card_send, account=account_send_obj)
                if not card_send_obj.is_activated:
                    raise exceptions.ValidationError("Карта отправителя заблокирована")

                token_card_send = card_send_obj.card_number

        except (Account.DoesNotExist, Card.DoesNotExist):
            raise exceptions.ValidationError("Неверные реквизиты отправителя")

        has_money = check_balance(account_send_obj, amount_money)
        if not has_money:
            raise exceptions.ValidationError("Недостаточно средств на счете отправителя.")

        description = {
            "From": {
                "card_number": token_card_send,
                "account_number": account_send,
                "full_name": str(user),
            },
            "To": {
                "card_number": card_number_recv,
                "account_number": account_recv,
                "full_name": None,
            },
            "amount_money": amount_money.to_eng_string(),
            "currency": account_send_obj.currency,
            "about": about
        }
        with transaction.atomic():
            operation = Operation.start_operation(description)
            self._response, tfa = TwoFactoryAuthentication.create_tfa(user, TFA.Event.Transfer,
                                                                      operation_id=operation.operation_id.hex)

        return tfa

    def get_response(self):
        return self._response


class UpdateTransferMoneySerializer(TwoFactoryAuthentication):
    _event = TFA.Event.Transfer

    def create(self, validated_data):
        self.check_tfa(validated_data=validated_data)

        user = UserContext.get_user()

        try:
            operation = Operation.objects.get(operation_id=self._payload['operation_id'])
        except Operation.DoesNotExist:
            raise exceptions.ValidationError("Незарегистрированная операция.")

        try:

            account_recv = operation.description["To"]["account_number"]
            card_number_recv = operation.description["To"]["card_number"]
            account_send = operation.description["From"]["account_number"]
            amount_money = Decimal(operation.description["amount_money"])

            user_recv = None

            account_send_obj = Account.objects.get(account_number=account_send, user=user)

            has_money = check_balance(account_send_obj, amount_money)
            if not has_money:
                raise exceptions.ValidationError("Недостаточно средств на счете отправителя.")

            with transaction.atomic():
                account_send_obj.balance = models.F("balance") - amount_money

                if account_recv is not None:
                    account_recv_obj = Account.objects.filter(account_number=account_recv).all()
                    if account_recv_obj.exists():
                        account_recv_obj = account_recv_obj[0]
                        amount = CurrencyConverter.convert(amount_money, account_send_obj.currency,
                                                           account_recv_obj.currency)

                        account_recv_obj.balance = models.F("balance") + amount
                        user_recv = str(account_recv_obj.user)
                        account_recv_obj.save()

                else:
                    card_recv_obj = Card.objects.filter(card_number=card_number_recv).all()
                    if card_recv_obj.exists():
                        card_recv_obj = card_recv_obj[0]
                        if not card_recv_obj.is_activated:
                            raise exceptions.ValidationError("Карта получателя заблокирована")
                        account_recv_obj = card_recv_obj.account
                        amount = CurrencyConverter.convert(amount_money, account_send_obj.currency,
                                                           account_recv_obj.currency)
                        account_recv_obj.balance = models.F("balance") + amount
                        user_recv = str(account_recv_obj.user)
                        account_recv = account_recv_obj.account_number
                        account_recv_obj.save()

                account_send_obj.save()

        except exceptions.ValidationError as ex:
            Operation.end_operation(operation, status=Operation.Status.FAILED)
            raise ex

        except Exception as ex:
            logging.exception(ex)
            Operation.end_operation(operation, status=Operation.Status.FAILED)
            self._response = {"status_operation": Operation.Status.FAILED}
        else:
            operation.description["To"]["full_name"] = user_recv
            operation.description["To"]["account_number"] = account_recv
            Operation.end_operation(operation, status=Operation.Status.SUCCESS)
            self._response = {"status_operation": Operation.Status.SUCCESS}

        return operation

    def get_response(self):
        return self._response
