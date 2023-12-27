from rest_framework.generics import ListAPIView
from ..models import ATM
from .. import serializers


class ATMAPIView(ListAPIView):
    queryset = ATM.objects.all()
    serializer_class = serializers.ATMSerializer
