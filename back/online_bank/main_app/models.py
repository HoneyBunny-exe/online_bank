import uuid
from django.db import models, DatabaseError
from utils import custom_validators, algorithms
import config


class User(models.Model):
    class Sex(models.TextChoices):
        MALE = 'male', 'Мужской'
        FEMALE = 'female', 'Женский'

    first_name = models.CharField(max_length=255, verbose_name='Имя',
                                  validators=(custom_validators.validate_russian_text,))
    second_name = models.CharField(max_length=255, verbose_name='Фамилия',
                                   validators=(custom_validators.validate_russian_text,))
    third_name = models.CharField(max_length=255, verbose_name='Отчество',
                                  validators=(custom_validators.validate_russian_text,))
    sex = models.TextField(choices=Sex.choices, verbose_name='Пол')
    birthday = models.DateField(verbose_name='День рождения')
    phone_number = models.CharField(max_length=16, validators=[custom_validators.validate_phone_number],
                                    verbose_name='Номер телефона')
    email = models.EmailField(null=True, verbose_name='Email')
    other_info = models.JSONField(verbose_name='Дополнительная информация')

    def __str__(self):
        return f"{self.second_name}  {self.first_name} {self.third_name}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Account(models.Model):
    class TypeAccount(models.TextChoices):
        CREDIT = 'credit', 'Кредитный'
        DEBIT = 'debit', 'Расcчётный'

    type_account = models.TextField(choices=TypeAccount.choices, verbose_name='Тип счёта')
    account_number = models.CharField(max_length=20, unique=True, verbose_name='Номер счета',
                                      validators=[custom_validators.validate_account_number])
    currency = models.CharField(max_length=3, choices=config.allow_currency_name.items(), verbose_name='Валюта')
    balance = models.DecimalField(max_digits=32, decimal_places=2, default=0, verbose_name='Баланс')
    user = models.ForeignKey('User', on_delete=models.PROTECT, related_name='accounts', verbose_name="Клиент")

    class Meta:
        verbose_name = 'счёт'
        verbose_name_plural = 'счёта'

    @staticmethod
    def create_account(type_account, currency, user):
        return Account(
            type_account=type_account,
            account_number=algorithms.create_new_account(currency),
            currency=currency,
            user=user
        )

    def __str__(self):
        return (f"{self.user.second_name.capitalize()} {self.user.first_name.capitalize()} "
                f"{self.user.third_name.capitalize()}/{self.account_number}")


class Contract(models.Model):
    contract_number = models.TextField(unique=True, verbose_name='Номер контракта')
    description = models.JSONField()
    account = models.OneToOneField('Account', on_delete=models.PROTECT, related_name='contract')

    class Meta:
        verbose_name = 'контракт'
        verbose_name_plural = 'контракты'

    @staticmethod
    def create_contract(account, /, percent_rate='', grace_period='', max_debt_amount=''):
        if account.type_account == Account.TypeAccount.CREDIT:
            if not all((percent_rate, grace_period, max_debt_amount)):
                raise DatabaseError("Invalid data entered")
            desc = {
                'url_scans': '',
                'description': {
                    "debt_arrear": config.DEBT_ARRER,
                    "percent_rate": percent_rate,
                    "grace_period": grace_period
                },
                "max_debt_amount": max_debt_amount
            }
        else:
            desc = {'url_scans': ''}

        return Contract(
            contract_number=algorithms.create_new_contract(account.type_account),
            description=desc,
            account=account
        )

    def __str__(self):
        return f"{self.contract_number}"


class Card(models.Model):
    token_card = models.UUIDField(primary_key=True, default=uuid.uuid4)
    card_number = models.CharField(max_length=16, unique=True,
                                   validators=[custom_validators.validate_card_number], verbose_name='Номер карты')
    init_datetime = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField(verbose_name='Дата окончания')
    is_activated = models.BooleanField(default=True, verbose_name="Статус")
    pin_hash = models.CharField(null=True)
    cvc_hash = models.CharField(verbose_name='CVC код')
    payment_system = models.CharField(max_length=255,
                                      choices=config.allow_payment_system_list, verbose_name='Платежная система')
    account = models.ForeignKey('Account', on_delete=models.PROTECT, related_name='cards')

    class Meta:
        verbose_name = 'карта'
        verbose_name_plural = 'карты'

    @staticmethod
    def create_card(account, /, payment_system):
        return Card(
            card_number=algorithms.create_new_card(payment_system),
            end_date=algorithms.get_end_date_for_card(),
            cvc_hash=algorithms.create_cvc_code(),
            payment_system=payment_system,
            account=account
        )

    def __str__(self):
        return f'{self.account}/{self.card_number}'


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
    longitude = models.FloatField(verbose_name='Долгота')
    latitude = models.FloatField(verbose_name='Широта')
    description = models.JSONField()

    class Meta:
        verbose_name = 'Отделение/Банкомат'
        verbose_name_plural = 'Отделения/Банкоматы'

    def __str__(self):
        return f'{self.description["address"]}'


class Authorization(models.Model):
    login = models.CharField(max_length=255, primary_key=True)
    password = models.CharField()
    salt = models.CharField()
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='auth_user')


class TFA(models.Model):
    auth_token = models.CharField(primary_key=True)
    confirm_code = models.CharField()
    expired_datetime_code = models.DateTimeField()
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='user_tfa')
