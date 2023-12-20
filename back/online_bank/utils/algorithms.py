import config
from config import BankConfig, allow_currency_code, allow_payment_system
import datetime
import json
import random
import base64


def lune_algorithm(arr_n: list[int], arr_k: list[int], length: int, weight: int = 0) -> int:
    sum_numbers = 0
    for i in range(length):
        p_i = arr_n[i] * arr_k[i]
        sum_numbers += p_i if p_i <= weight else p_i - weight

    return sum_numbers % 10


def init_arr_n(digits_string: str) -> list[int]:
    arr_n = [int(digit) for digit in digits_string]
    return arr_n


def calculate_account_check_sum(account_number: str) -> int:
    bank_id = BankConfig.get_bik()
    arr_n = init_arr_n(bank_id[-3:] + account_number)
    length = len(arr_n)
    arr_k = [7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1]
    res = lune_algorithm(arr_n, arr_k, length)
    return res * arr_k[11] % 10


def calculate_card_check_sum(card_number: str) -> int:
    arr_n = init_arr_n(card_number)
    length = len(arr_n)
    arr_k = [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    return (10 - lune_algorithm(arr_n, arr_k, length, weight=9)) % 10


def create_new_account(currency: str) -> str:
    prefix = "40817"
    init_number = 14159265358
    currency_code = allow_currency_code[currency]
    account_number = "%011d" % (init_number ^ BankConfig.get_account_counter())
    row_number = ''.join((prefix, currency_code, '0', account_number[-11:]))
    check_number = str(calculate_account_check_sum(row_number))
    BankConfig.increment_account_counter()
    return ''.join((prefix, currency_code, check_number, account_number[-11:]))


def create_new_card(payment_system: str) -> str:
    init_number = 718281828
    BIN = BankConfig.get_bin()
    payment_system_code = allow_payment_system[payment_system]
    card_number = "%09d" % (init_number ^ BankConfig.get_card_counter())
    row_number = ''.join((payment_system_code, BIN, card_number[-9:], "0"))
    check_number = str(calculate_card_check_sum(row_number))
    BankConfig.increment_card_counter()
    return ''.join((payment_system_code, BIN, card_number[-9:], check_number))


def create_new_contract(type_contract: str) -> str:
    init_number = 6180339887
    current_date = datetime.date.today().isoformat()
    contract_number = "%010d" % (init_number ^ BankConfig.get_contract_counter())
    BankConfig.increment_contract_counter()
    return "/".join((type_contract, current_date, contract_number))


def create_cvc_code():
    digit_1 = random.randint(0, 9)
    digit_2 = random.randint(0, 9)
    digit_3 = random.randint(0, 9)
    return f"{digit_1}{digit_2}{digit_3}"


def get_end_date_for_card():
    today = datetime.date.today()
    year = today.year
    return today.replace(year=year + config.ACTIVE_CARD_PERIOD_IN_YEARS)


def serialize_to_json(data: dict):
    serialized_data = json.dumps(data)
    return serialized_data.encode('UTF-8')


def deserialize_to_dict(row_json):
    serialized_data = json.loads(row_json)
    return serialized_data
