from rest_framework.response import Response
from rest_framework.views import APIView
from .. import serializers
from ..auth import JWTAuthentication


class JWTAuthenticationAPIView(APIView):
    authentication_classes = (JWTAuthentication,)


class FilterMixin:
    def filter(self, request, filter_fields):
        filter_dict = {}
        for key, field in filter_fields:
            value = request.GET.get(field, None)
            if value is None:
                continue
            filter_dict.update({key: value})

        return filter_dict


class UpdateJWTAPIView(APIView):

    def post(self, request):
        serializer = serializers.UpdateJWTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())
