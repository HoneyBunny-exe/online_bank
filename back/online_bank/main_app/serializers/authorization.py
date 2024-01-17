from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import exceptions
import config
from main_app.models import Authorization, Session, TFA
from main_app.serializers import TwoFactoryAuthentication
from utils import auth_tools, custom_validators, algorithms, UserContext


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


class CreateChangeAuthSerializer(serializers.Serializer):
    new_login = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=255, required=False)
    re_password = serializers.CharField(max_length=255, required=False
                                        )
    _response = None

    @staticmethod
    def check_password(password, re_password):
        if password != re_password:
            raise exceptions.ValidationError("Поле password и поле re_password должны совпадать.")

    def validate(self, attrs):
        login = attrs.get("new_login", None)
        password = attrs.get("password", None)
        re_password = attrs.get("re_password", None)
        if not (login or (password and re_password)):
            raise exceptions.ValidationError("Необходимо указать новый логин или новый пароль.")
        if password is not None:
            self.check_password(password, re_password)
        return attrs

    def create(self, validated_data):
        user = UserContext.get_user()
        new_login = validated_data.get('new_login', None)
        new_password = validated_data.get('password', None)
        try:

            auth = Authorization.objects.get(user=user)

        except Authorization.DoesNotExist:

            raise exceptions.ValidationError("Вы не клиент нашего банка")

        if new_login is not None:
            has_login = Authorization.objects.filter(login=new_login).all().exists()
            if has_login:
                raise exceptions.ValidationError(f"{new_login} уже занят.")
        else:
            new_login = auth.login

        password_hash = auth.password
        print(password_hash)
        salt = auth.salt
        if new_password is not None:
            password_hash, salt = auth_tools.calculate_password_hash(new_password)
        print(password_hash)

        self._response, tfa = TwoFactoryAuthentication.create_tfa(user=user, event=TFA.Event.ChangeAuth, login=new_login,
                                                                  password_hash=password_hash, salt=salt)
        return tfa

    def get_response(self):
        return self._response


class UpdateChangeAuthSerializer(TwoFactoryAuthentication):
    _event = TFA.Event.ChangeAuth

    def create(self, validated_data):
        self.check_tfa(validated_data=validated_data)

        user = UserContext.get_user()
        print(self._payload)
        try:
            auth = Authorization.objects.get(user=user)
            auth.login = self._payload['login']
            auth.password = self._payload['password_hash']
            auth.salt = self._payload['salt']
            auth.save()
        except (IntegrityError, Authorization.DoesNotExist):
            raise exceptions.ValidationError(f"{self._payload['login']} уже занят")

        self._response = {
            "status": "success"
        }

        return auth

    def get_response(self):
        return self._response
