from django.core.exceptions import ValidationError
from .algorithms import calculate_card_check_sum, calculate_account_check_sum

__all__ = [
    "validate_phone_number",
    "validate_account_number",
    "validate_card_number"
]


def validate_phone_number(phone_number: str):
    length = len(phone_number)
    if length < 11 or length > 16 or not (phone_number[1:].isdigit() and phone_number[0] == "+"):
        raise ValidationError("Перепроверьте  введенные данные")


def validate_russian_text(russian_text: str):
    allow_letters = set('ЙЦУКЕНГШЩЗХФЫВАПРОЛДЖЭЯЧСМИТБЮЁёйцукенгшщзхъфывапролджэячсмитбюь')
    if not set(russian_text).issubset(allow_letters):
        raise ValidationError("Ипользуйте только символы русского (православного) алфавита")


def validate_account_number(account_number: str):
    length = len(account_number)
    if length == 20 and account_number.isdigit():
        check_num = calculate_account_check_sum(account_number)
        if check_num == 0:
            return

    raise ValidationError(
        "%(account_number)s is not a account number",
        params={"account_number": account_number}
    )


def validate_card_number(card_number: str):
    length = len(card_number)
    if length == 16 and card_number.isdigit():
        check_num = calculate_card_check_sum(card_number)
        if check_num == 0:
            return

    raise ValidationError(
        "%(card_number)s is not a card number",
        params={"card_number": card_number}
    )
