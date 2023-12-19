from rest_framework import serializers
from ..models import ATM


class ATMSerializer(serializers.ModelSerializer):
    class Meta:
        model = ATM
        fields = ('longitude', 'latitude', 'description')
