from django.core.exceptions import ValidationError


def validate_phone_code(phone_code: str):
    if len(phone_code) < 1 or len(phone_code) > 3 or not phone_code.isdigit():
        raise ValidationError(
            "%(phone_code)s is not a phone code",
            params={"phone_code": phone_code}
        )


def validate_phone_number(phone_code: str):
    if len(phone_code) < 1 or len(phone_code) > 14 or not phone_code.isdigit():
        raise ValidationError(
            "%(phone_code)s is not a phone number",
            params={"phone_code": phone_code}
        )
