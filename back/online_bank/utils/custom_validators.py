from django.core.exceptions import ValidationError
from .algorithms import exec_card_check_number, exec_account_check_number


def validate_phone_code(phone_code: str):
    length = len(phone_code)
    if length < 1 or length > 3 or not phone_code.isdigit():
        raise ValidationError(
            "%(phone_code)s is not a phone code",
            params={"phone_code": phone_code}
        )


def validate_phone_number(phone_number: str):
    length = len(phone_number)
    if length < 1 or length > 14 or not phone_number.isdigit():
        raise ValidationError(
            "%(phone_number)s is not a phone number",
            params={"phone_number": phone_number}
        )


def validate_account_number(account_number: str):
    length = len(account_number)
    if length == 20 and account_number.isdigit():
        check_num = exec_account_check_number(account_number)
        if check_num == 0:
            return

    raise ValidationError(
        "%(account_number)s is not a account number",
        params={"account_number": account_number}
    )


def validate_card_number(card_number: str):
    length = len(card_number)
    if length == 16 and card_number.isdigit():
        check_num = exec_card_check_number(card_number)
        if check_num == 0:
            return

    raise ValidationError(
        "%(card_number)s is not a card number",
        params={"card_number": card_number}
    )
