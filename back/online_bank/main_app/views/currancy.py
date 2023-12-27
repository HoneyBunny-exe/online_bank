from rest_framework.response import Response
from rest_framework.views import APIView
from utils import CurrencyParser


class CurrencyAPIView(APIView):

    def get(self, request):
        return Response(CurrencyParser.get_currency_prices())
