from rest_framework.response import Response
from .. import serializers
from .JWT import JWTAuthenticationAPIView


class TransferMoneyAPIView(JWTAuthenticationAPIView):
    def post(self, request):
        serializer = serializers.CreateTransferMoneySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())

    def put(self, request):
        serializer = serializers.UpdateTransferMoneySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())
