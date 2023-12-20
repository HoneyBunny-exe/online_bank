import base64
import binascii

from django.core.exceptions import ValidationError as ModelError
from rest_framework.exceptions import ValidationError as APIError

from . import auth_tools
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
            raise APIError("Перепроверьте  введенные данные")
        else:
            raise ModelError("Перепроверьте  введенные данные")


def validate_russian_text(russian_text: str, is_api=False):
    allow_letters = set('ЙЦУКЕНГШЩЗХФЫВАПРОЛДЖЭЯЧСМИТБЮЁёйцукенгшщзхъфывапролджэячсмитбюь')
    if not set(russian_text).issubset(allow_letters):
        if is_api:
            raise APIError("Ипользуйте только символы русского (православного) алфавита")
        else:
            raise ModelError("Ипользуйте только символы русского (православного) алфавита")


def validate_account_number(account_number: str, is_api=False):
    length = len(account_number)
    if length == 20 and account_number.isdigit():
        check_num = calculate_account_check_sum(account_number)
        if check_num == 0:
            return
    if is_api:
        raise APIError(f"Счет {account_number} не валиден")
    else:
        raise ModelError(
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
        raise APIError()
    else:
        raise ModelError(
            "%(card_number)s is not a card number",
            params={"card_number": card_number}
        )


def validate_token(token: str, is_api=False):
    error_message = "Недействительный токен."
    try:
        binary_data, sign = auth_tools.parse_token(token)
    except ValueError:
        if is_api:
            raise APIError(error_message)
        else:
            raise ModelError(error_message)

    has_verified = auth_tools.verify_token(binary_data, sign)
    if has_verified:
        return binary_data, token

    if is_api:
        raise APIError(error_message)
    else:
        raise ModelError(error_message)
