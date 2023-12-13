import os

DEBT_ARRER = "0.1"
ACTIVE_CARD_PERIOD_IN_YEARS = 6


class BankConfig:
    def __new__(cls, *args, **kwargs):
        return

    @staticmethod
    def get_bik():
        bik = os.environ.get("BIK")
        if bik is None:
            bik = os.environ["BIK"] = '044544512'
        return bik

    @staticmethod
    def get_bin():
        bin_ = os.environ.get("BIN")
        if bin_ is None:
            bin_ = os.environ["BIN"] = '59913'
        return bin_

    @staticmethod
    def _get_counter(name: str):
        counter = os.environ.get(name)
        if counter is None:
            counter = os.environ[name] = "6"
        return int(counter)

    @staticmethod
    def _increment_counter(name: str):
        counter = os.environ.get(name)
        if counter is None:
            os.environ[name] = "0"
        else:
            counter = str(int(counter) + 1)
            os.environ[name] = counter

    @classmethod
    def get_card_counter(cls):
        return cls._get_counter('CARD_COUNTER')

    @classmethod
    def get_account_counter(cls):
        return cls._get_counter('ACCOUNT_COUNTER')

    @classmethod
    def get_contract_counter(cls):
        return cls._get_counter('CONTRACT_COUNTER')

    @classmethod
    def increment_card_counter(cls):
        cls._increment_counter('CARD_COUNTER')

    @classmethod
    def increment_account_counter(cls):
        return cls._increment_counter('ACCOUNT_COUNTER')

    @classmethod
    def increment_contract_counter(cls):
        return cls._increment_counter('CONTRACT_COUNTER')


allow_currency = {
    "RUB": 810,
    "USD": 840,
    "KZT": 398,
    "GBP": 826,
    "BYB": 112,
    "PLZ": 616,
    "JPY": 392,
    "CNY": 156,
}

allow_payment_system = {
    "MasterCard": 5,
    "Visa": 4,
    "China Union Pay": 6,
    "МИР": 2,
}

allow_payment_system_list = [(_, _) for _ in allow_payment_system.keys()]
allow_currency_list = [(_, _) for _ in allow_currency.keys()]

json_user_template = {
    "passport_data": "",
}

json_contract_template = {
    "url_scan": "",
    "description": {
        "debt_arrear": "",
        "percent_rate": "",
        "grace_period": ""
    },
    "max_debt_amount": "",
    "end_current_grace_period": ""
}

json_operations_template = {
    "From": {
        "card_number": "",
        "account_number": "",
        "full_name": "",
    },
    "To": {
        "card_number": "",
        "account_number": "",
        "full_name": "",
    },
    "payment_system": "",
    "amount_money": "",
    "description": ""
}
