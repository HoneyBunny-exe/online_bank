import datetime

from django.utils import timezone
from rest_framework import serializers
from rest_framework import exceptions
from django.db import transaction

import config
from .models import ATM, Account, Authorization, Registration
from utils import custom_validators, auth_tools


class ATMSerializer(serializers.ModelSerializer):
    class Meta:
        model = ATM
        fields = ('longitude', 'latitude', 'description')


class CreateRegistrationSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=20, min_length=20)
    login = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    re_password = serializers.CharField(max_length=255)
    _response = None

    def validate_password(self, value):
        if value != self.initial_data['re_password']:
            raise exceptions.ValidationError("Поле password и поле re_password должны совпадать")
        return value

    def validate_account(self, value):
        custom_validators.validate_account_number(value, is_api=True)
        return value

    def create(self, validated_data):
        try:

            account = Account.objects.get(account_number=validated_data['account'])

        except Account.DoesNotExist:

            raise exceptions.ValidationError()

        password_hash, salt = auth_tools.calculate_password_hash(validated_data['password'])
        user = account.user
        login = validated_data['login']
        registration_token = auth_tools.create_auth_token(login)
        confirm_code = auth_tools.create_confirm_code()
        expired_datetime_code = datetime.datetime.utcnow() + datetime.timedelta(
            seconds=config.INTERVAL_CONFIRM_CODE_IN_SECONDS)
        regis = Registration.objects.create(registration_token=registration_token, login=login, password=password_hash,
                                            salt=salt,confirm_code=confirm_code, expired_datetime_code=expired_datetime_code,
                                            user=user)
        self._response = {
            "registration_token": registration_token,
            "confirm_code": confirm_code,
            "life_interval_in_seconds": config.INTERVAL_CONFIRM_CODE_IN_SECONDS
        }
        return regis

    def get_response(self):
        return self._response


class UpdateRegistrationSerializer(serializers.Serializer):
    registration_token = serializers.CharField()
    confirm_code = serializers.CharField()

    _response = None

    def create(self, validated_data):
        registration_token = validated_data['registration_token']
        current_datetime = datetime.datetime.utcnow()

        try:
            register = Registration.objects.get(registration_token=registration_token)
        except Registration.DoesNotExist:
            raise exceptions.ValidationError()

        confirm_code = register.confirm_code
        if register.expired_datetime_code > current_datetime or confirm_code != validated_data['confirm_code']:
            raise exceptions.ValidationError()

        # user = register.user
        # login = validated_data['login']
        # password = register.password
        # salt = register.salt

        self._response = {
            "Success_register": True,
            "code": "1234567"
        }
        return register

    def get_response(self):
        return self._response
