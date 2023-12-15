from django.core.exceptions import ValidationError as model_error
from rest_framework.exceptions import ValidationError as api_arror
from .algorithms import calculate_card_check_sum, calculate_account_check_sum

__all__ = [
    "validate_phone_number",
    "validate_account_number",
    "validate_card_number"
]


def validate_phone_number(phone_number: str, is_api=False):
    length = len(phone_number)
    if length < 11 or length > 16 or not (phone_number[1:].isdigit() and phone_number[0] == "+"):
        if is_api:
            raise api_arror("Перепроверьте  введенные данные")
        else:
            raise model_error("Перепроверьте  введенные данные")


def validate_russian_text(russian_text: str, is_api=False):
    allow_letters = set('ЙЦУКЕНГШЩЗХФЫВАПРОЛДЖЭЯЧСМИТБЮЁёйцукенгшщзхъфывапролджэячсмитбюь')
    if not set(russian_text).issubset(allow_letters):
        if is_api:
            raise api_arror("Ипользуйте только символы русского (православного) алфавита")
        else:
            raise model_error("Ипользуйте только символы русского (православного) алфавита")


def validate_account_number(account_number: str, is_api=False):
    length = len(account_number)
    if length == 20 and account_number.isdigit():
        check_num = calculate_account_check_sum(account_number)
        if check_num == 0:
            return
    if is_api:
        raise api_arror()
    else:
        raise model_error(
            "%(account_number)s is not a account number",
            params={"account_number": account_number}
        )


def validate_card_number(card_number: str, is_api=False):
    length = len(card_number)
    if length == 16 and card_number.isdigit():
        check_num = calculate_card_check_sum(card_number)
        if check_num == 0:
            return
    if is_api:
        raise api_arror()
    else:
        raise model_error(
            "%(card_number)s is not a card number",
            params={"card_number": card_number}
        )
