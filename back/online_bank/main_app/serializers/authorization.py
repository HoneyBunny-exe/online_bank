import base64

from rest_framework import serializers
from rest_framework import exceptions
import config
from main_app.models import Authorization, Session, TFA
from main_app.serializers import TwoFactoryAuthentication
from utils import auth_tools, custom_validators, algorithms


class CreateAuthorizationSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    _response = None

    def create(self, validated_data):
        login = validated_data['login']
        row_password = validated_data['password']
        try:

            auth = Authorization.objects.get(login=login)

        except Authorization.DoesNotExist:

            raise exceptions.ValidationError(f'Пользователя с логином {login} не существует')

        verified = auth_tools.verify_passwords(auth.password, auth.salt, row_password)
        if verified:
            self._response, tfa = TwoFactoryAuthentication.create_tfa(user=auth.user, event=TFA.Event.Authorization)
            return tfa

        raise exceptions.ValidationError('Неправильно введенные данные.')

    def get_response(self):
        return self._response


class UpdateAuthorizationSerializer(TwoFactoryAuthentication):
    _event = TFA.Event.Authorization

    def create(self, validated_data):
        user = self.check_tfa(validated_data=validated_data)

        access_token, refresh_token = Session.create_session(user)
        self._response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "life_expectancy_api_token_in_seconds": config.INTERVAL_API_TOKEN_IN_SECONDS
        }
        return user

    def get_response(self):
        return self._response


class UpdateJWTSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    _response = None
    _payload = None

    def validate_refresh_token(self, refresh_token):
        binary_data, token = custom_validators.validate_token(refresh_token, is_api=True)
        self._payload = algorithms.deserialize_to_dict(binary_data)
        return token

    def create(self, validated_data):
        refresh_token = validated_data['refresh_token']
        error_msg = 'Недействительный токен.'
        try:

            session = Session.objects.get(api_id=self._payload["uuid"])

        except Session.DoesNotExist:
            raise exceptions.ValidationError(error_msg)

        if auth_tools.compare_digest(session.refresh_token, refresh_token):
            access_token, refresh_token = Session.update_session(session)

            self._response = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "life_expectancy_api_token_in_seconds": config.INTERVAL_API_TOKEN_IN_SECONDS
            }
            return session

        raise exceptions.ValidationError(error_msg)

    def get_response(self):
        return self._response
