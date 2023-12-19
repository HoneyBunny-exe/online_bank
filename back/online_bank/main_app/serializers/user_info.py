from rest_framework import serializers
from ..models import User


class UserInfoSerializer(serializers.ModelSerializer):
    login = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'second_name', 'third_name', 'sex', 'birthday', 'phone_number', 'email', 'login')

    def get_login(self, obj):
        return obj.auth_user.login
