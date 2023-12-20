from django.core.exceptions import ValidationError as ModelError
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as APIError
from ..models import Account, Card, Operation
from .. import serializers
from . import FilterMixin, JWTAuthenticationAPIView


class OperationInfoAPIView(JWTAuthenticationAPIView, FilterMixin):
    def get(self, request):
        user = request.user
        account_number = request.GET.get("account_number", None)
        if account_number is None:
            raise APIError("Неверные параметры запроса")

        token_card = request.GET.get("token_card", None)

        try:
            account = Account.objects.get(account_number=account_number, user=user)

            filter_dict_from = {"description__From__account_number": account.account_number}
            filter_dict_to_account = {"description__To__account_number": account.account_number}
            filter_dict_to_card = {}
            filter_dict = self.filter(request,
                                      [('status_operation', 'status_operation'), ('description__currency', 'currency')])

            if token_card is not None:
                card = Card.objects.get(token_card=token_card, account=account)
                filter_dict_from.update({'description__From__card_number': card.card_number})
                filter_dict_to_card.update({'description__To__card_number': card.card_number})

            operations = Operation.objects.filter(Q(**filter_dict_from) | Q(**filter_dict_to_account) | Q(**filter_dict_to_card), **filter_dict).all()
            return Response(serializers.OperationInfoSerializer(operations, many=True).data)
        except (ModelError, Account.DoesNotExist, Card.DoesNotExist):
            raise APIError("Неверные параметры запроса")
