from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError
from utils import CurrencyParser
from .models import ATM, Account, Card
from . import serializers


class ATMAPIView(ListAPIView):
    queryset = ATM.objects.all()
    serializer_class = serializers.ATMSerializer


class CurrencyAPIView(APIView):
    def get(self, request):
        return Response(CurrencyParser.get_currency_prices())


class HasAccountAPIView(APIView):
    def get(self, request):
        account = request.GET.get('account_number', None)
        if account is None:
            raise ValidationError('Required parameter account_number')
        res = Account.objects.filter(account_number=account).exists()
        return Response({"has_account": res})


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = serializers.CreateRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())

    def put(self, request):
        serializer = serializers.UpdateRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())



