from rest_framework import serializers
from rest_framework import exceptions
from main_app.models import TFA
import config
from .TFA import TwoFactoryAuthentication
from main_app.models import Account, Authorization, Session
from utils import custom_validators, auth_tools
from django.db import IntegrityError, transaction


class CreateRegistrationSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=20, min_length=20)
    login = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    re_password = serializers.CharField(max_length=255)
    _response = None

    def validate_password(self, password):
        if password != self.initial_data['re_password']:
            raise exceptions.ValidationError("Поле password и поле re_password должны совпадать.")
        return password

    def validate_account(self, account):
        custom_validators.validate_account_number(account, is_api=True)
        return account

    def validate_login(self, login):
        has_login = Authorization.objects.filter(login=login).exists()
        if has_login:
            raise exceptions.ValidationError(f"{login} уже занат.")
        return login

    def create(self, validated_data):
        try:

            account = Account.objects.get(account_number=validated_data['account'])

        except Account.DoesNotExist:

            raise exceptions.ValidationError("Данный счет не принадлежит нашему банку.")

        user = account.user
        has_auth = Authorization.objects.filter(user_id=user.pk).exists()
        if has_auth:
            raise exceptions.ValidationError("Вы уже зарегистрированы")

        password_hash, salt = auth_tools.calculate_password_hash(validated_data['password'])
        login = validated_data['login']

        self._response, tfa = TwoFactoryAuthentication.create_tfa(user=user, event=TFA.Event.Registration, login=login,
                                                                  password_hash=password_hash, salt=salt)
        return tfa

    def get_response(self):
        return self._response


class UpdateRegistrationSerializer(TwoFactoryAuthentication):
    _event = TFA.Event.Registration

    def create(self, validated_data):
        user = self.check_tfa(validated_data=validated_data)

        with transaction.atomic():
            try:
                Authorization.objects.create(
                    login=self._payload['login'],
                    password=self._payload['password_hash'],
                    salt=self._payload['salt'],
                    user=user
                )
            except IntegrityError:
                raise exceptions.ValidationError(f"{self._payload['login']} уже занят")

            access_token, refresh_token = Session.create_session(user)
            self._response = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expiration_access_token_in_seconds": config.INTERVAL_API_TOKEN_IN_SECONDS
            }

        return user

    def get_response(self):
        return self._response
