from rest_framework.response import Response
from rest_framework.views import APIView
from .. import serializers
from . import JWTAuthenticationAPIView


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


class ChangeAuthAPIView(JWTAuthenticationAPIView):

    def post(self, request):
        serializer = serializers.CreateChangeAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())

    def put(self, request):
        serializer = serializers.UpdateChangeAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())
