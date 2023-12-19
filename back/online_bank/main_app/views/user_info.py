from rest_framework.response import Response
from .. import serializers
from . import JWTAuthenticationAPIView


class UserInfoAPIView(JWTAuthenticationAPIView):
    def get(self, request):
        user = request.user
        return Response(serializers.UserInfoSerializer(user).data)
