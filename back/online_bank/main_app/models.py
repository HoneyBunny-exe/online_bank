from django.db import models
from utils import custom_validators


class User(models.Model):
    class Sex(models.TextChoices):
        MALE = 'male', 'мужской'
        FEMALE = 'female', 'женский'

    first_name = models.TextField()
    second_name = models.TextField()
    third_name = models.TextField()
    sex = models.TextField(choices=Sex.choices)
    phone_code = models.CharField(max_length=3, validators=[custom_validators.validate_phone_code])
    phone_number = models.CharField(max_length=14, validators=[custom_validators.validate_phone_number])
    email = models.EmailField(null=True)
    other_info = models.JSONField()


class Authorization(models.Model):
    login = models.CharField(max_length=255, primary_key=True)
    password = models.BinaryField()
    salt = models.BinaryField()
    user = models.OneToOneField('User', on_delete=models.PROTECT, related_name='auth_user')


class Account(models.Model):
    class TypeAccount(models.TextChoices):
        CREDIT = 'credit', 'кредитный'
        DEBIT = 'debit', 'расcчётный'

    type_account = models.TextField(choices=TypeAccount.choices)
    account_number = models.CharField(max_length=20, unique=True,
                                      validators=[custom_validators.exec_account_check_number])
    currency = models.CharField(max_length=3)
    balance = models.DecimalField(max_digits=32, decimal_places=2)
    user = models.ForeignKey('User', on_delete=models.PROTECT, related_name='accounts')


class Contract(models.Model):
    contract_number = models.TextField(unique=True)
    description = models.JSONField()
    account = models.OneToOneField('Account', on_delete=models.PROTECT, related_name='contract')


class Card(models.Model):
    card_number = models.CharField(max_length=16, primary_key=True,
                                   validators=[custom_validators.exec_card_check_number])
    init_datetime = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField()
    is_activated = models.BooleanField()
    token_card = models.UUIDField(unique=True)
    pin_hash = models.BinaryField(null=True)
    cvc_hash = models.BinaryField()
    payment_system = models.CharField(max_length=255)
    account = models.ForeignKey('Account', on_delete=models.PROTECT, related_name='cards')


class Operation(models.Model):
    class Status(models.TextChoices):
        SUCCESS = 'success'
        FAILED = 'failed'
        PENDING = 'pending'

    status_operation = models.TextField(choices=Status.choices)
    start_transaction = models.DateTimeField(auto_now_add=True)
    end_transaction = models.DateTimeField(null=True)
    description = models.JSONField()


class ATM(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    description = models.JSONField()
