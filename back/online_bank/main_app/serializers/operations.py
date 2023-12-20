from rest_framework import serializers, exceptions
from utils import UserContext, custom_validators
from ..models import Card, Operation


class OperationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('status_operation', 'start_transaction', 'end_transaction', 'description')
