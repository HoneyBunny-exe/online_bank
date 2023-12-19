from rest_framework import serializers
from django.db import transaction
import config
from ..models import Account, Contract
from utils import UserContext


currencies = config.allow_currency_name.items()


class AccountInfoSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('account_number', 'type_account', 'currency', 'balance', 'description')

    def get_description(self, obj):
        return obj.contract.description


class CreateAccountSerializer(serializers.Serializer):
    currency = serializers.ChoiceField(label='Валюта', choices=list(currencies))
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
