from rest_framework import serializers, exceptions
from utils import UserContext, custom_validators
from ..models import Card, Account
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
        return obj.get_name()

    def get_type_account(self, obj):
        return obj.account.type_account

    def get_currency(self, obj):
        return obj.account.currency

    def get_balance(self, obj):
        return obj.account.balance

    def get_account_number(self, obj):
        return obj.account.account_number


class CreateCardSerializer(serializers.Serializer):
    payment_system = serializers.ChoiceField(choices=allow_payment_system_list)
    account = serializers.CharField(max_length=20, min_length=20)
    _response = None

    def validate_account(self, account):
        custom_validators.validate_account_number(account, is_api=True)
        return account

    def create(self, validated_data):
        user = UserContext.get_user()
        try:
            account = Account.objects.get(account_number=validated_data['account'], user=user)
        except Account.DoesNotExist:
            raise exceptions.ValidationError("Недействительнный номер счета")

        card = Card.create_card(account, payment_system=validated_data["payment_system"])
        card.save()
        card_number = card.card_number
        self._response = {
            "account_number": account.account_number,
            "type_account": account.type_account,
            "currency": account.currency,
            "balance": account.balance,
            "card_name": card.get_name(),
            "token_card": card.token_card,
            "end_date": card.end_date,
            "is_activated": card.is_activated,
            "payment_system": card.payment_system,
        }
        return card

    def get_response(self):
        return self._response


class BlockCardSerializer(serializers.Serializer):
    token_card = serializers.UUIDField()
    is_activated = serializers.BooleanField()
    _response = None

    def create(self, validated_data):
        user = UserContext.get_user()
        try:
            card = Card.objects.get(account__user=user, token_card=validated_data["token_card"])
        except Card.DoesNotExist:
            raise exceptions.ValidationError("Недействительнный токен карты")

        card.is_activated = validated_data['is_activated']
        card.save()
        self._response = {"is_activated": card.is_activated}
        return card

    def get_response(self):
        return self._response

