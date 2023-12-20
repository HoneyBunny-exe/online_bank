from django.core.exceptions import ValidationError as ModelError
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as APIError
from ..models import Account
from .. import serializers
from . import FilterMixin, JWTAuthenticationAPIView
from rest_framework.views import APIView


class AccountInfoAPIView(JWTAuthenticationAPIView, FilterMixin):

    def get(self, request):
        try:
            user = request.user
            filter_dict = self.filter(request, (('account_number', 'account_number'), ('type_account', 'type_account'),
                                                ('currency', 'currency')))
            accounts = Account.objects.filter(user=user, **filter_dict).all()
            return Response(serializers.AccountInfoSerializer(accounts, many=True).data)
        except ModelError:
            raise APIError("Неверные параметры запроса")


class HasAccountAPIView(APIView):

    def get(self, request):
        account = request.GET.get('account_number', None)
        if account is None:
            raise APIError('Required parameter account_number')
        res = Account.objects.filter(account_number=account).exists()
        return Response({"has_account": res})


class CreateAccountAPIView(JWTAuthenticationAPIView):

    def post(self, request):
        serializer = serializers.CreateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())
