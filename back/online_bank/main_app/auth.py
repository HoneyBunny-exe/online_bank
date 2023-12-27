from datetime import datetime
from rest_framework import authentication
from rest_framework import exceptions
from utils.auth_tools import verify_jwt_token, TypeToken, parse_token
from utils.algorithms import deserialize_to_dict
from .models import Session
from utils import UserContext


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION', None)
        msg = "В доступе отказано"
        try:
            binary_data, jwt_sign = parse_token(jwt_token)
            verified = verify_jwt_token(binary_data, jwt_sign)
            if verified:
                data = deserialize_to_dict(binary_data)
                if data['type'] == TypeToken.ACCESS:
                    current_datetime = datetime.utcnow()
                    expiration_datetime = data["expiration_datetime"]
                    expiration_datetime = datetime.fromisoformat(expiration_datetime)
                    if current_datetime <= expiration_datetime:
                        session = Session.objects.get(api_id=data['uuid'])
                        user = session.user
                        UserContext.set_user(user)
                        return user, session

        except (ValueError, Session.DoesNotExist, KeyError):
            raise exceptions.AuthenticationFailed(msg)

        raise exceptions.AuthenticationFailed(msg)

