from django.core.exceptions import ValidationError as ModelError
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as APIError
from ..models import Card
from .. import serializers
from . import FilterMixin, JWTAuthenticationAPIView


class CardInfoAPIView(JWTAuthenticationAPIView, FilterMixin):
    def get(self, request):
        try:
            user = request.user
            filter_dict = self.filter(request, (('token_card', 'token_card'), ('is_activated', 'is_activated'),
                                                ('payment_system', 'payment_system'),
                                                ('account__account_number', 'account_number'), ('account__type_account', 'type_account'),
                                                ('account__currency', 'currency')))
            cards = Card.objects.filter(account__user=user, **filter_dict).select_related("account").all()
            return Response(serializers.CardInfoSerializer(cards, many=True).data)
        except ModelError:
            raise APIError("Неверные параметры запроса")


class CreateCardAPIView(JWTAuthenticationAPIView):
    def post(self, request):
        serializer = serializers.CreateCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())


class BlockCardAPIView(JWTAuthenticationAPIView):
    def post(self, request):
        serializer = serializers.BlockCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.get_response())
