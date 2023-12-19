from rest_framework import serializers
from ..models import Account


class AccountInfoSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('account_number', 'type_account', 'currency', 'balance', 'description')

    def get_description(self, obj):
        return obj.contract.description
