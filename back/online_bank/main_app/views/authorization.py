from rest_framework.response import Response
from rest_framework.views import APIView
from .. import serializers


class AuthorizationAPIView(APIView):

    def post(self, request):
        serializer = serializers.CreateAuthorizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())

    def put(self, request):
        serializer = serializers.UpdateAuthorizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())
