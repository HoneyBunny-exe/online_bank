from django.db import transaction
from rest_framework import serializers
from utils import UserContext
from ..models import Card
from config import allow_payment_system_list


class CardInfoSerializer(serializers.ModelSerializer):
    card_name = serializers.SerializerMethodField()
    type_account = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    account_number = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ('account_number', 'type_account', 'currency', 'balance', 'card_name',
                  'token_card', 'end_date', 'is_activated', 'payment_system')

    def get_card_name(self, obj):
        card_number = obj.card_number
        return card_number[:4] + "*" * 8 + card_number[-4:]

    def get_type_account(self, obj):
        return obj.account.type_account

    def get_currency(self, obj):
        return obj.account.currency

    def get_balance(self, obj):
        return obj.account.balance

    def get_account_number(self, obj):
        return obj.account.account_number


class CreateAccountSerializer(serializers.Serializer):
    payment_system = serializers.ChoiceField(choices=allow_payment_system_list)
    _response = None

    def create(self, validated_data):
        user = UserContext.get_user()
        with transaction.atomic():
            account = Account.create_account(Account.TypeAccount.DEBIT, validated_data["currency"], user)
            contract = Contract.create_contract(account)
            account.save()
            contract.save()

        self._response = {
            "account_number": account.account_number,
            "type_account": account.type_account,
            "currency": account.currency,
            "balance": account.balance,
            "description": contract.description
        }
        return account

    def get_response(self):
        return self._response
