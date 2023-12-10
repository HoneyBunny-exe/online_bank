def lune_algorithm(arr_n: list[int], arr_k: list[int], length: int, weight: int = 0) -> int:
    sum_numbers = 0
    for i in range(length):
        p_i = arr_n[i] * arr_k[i]
        sum_numbers += p_i if p_i <= weight else p_i - weight

    return sum_numbers % 10


def init_arr_n(digits_string: str) -> list[int]:
    arr_n = [int(digit) for digit in digits_string]
    return arr_n


def exec_account_check_number(account_number: str) -> int:
    bank_id = '044544512'  # add BIK in environment
    arr_n = init_arr_n(bank_id[-3:] + account_number)
    length = len(arr_n)
    arr_k = [7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1]
    return lune_algorithm(arr_n, arr_k, length)


def exec_card_check_number(card_number: str) -> int:
    arr_n = init_arr_n(card_number)
    length = len(arr_n)
    arr_k = [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    return lune_algorithm(arr_n, arr_k, length, weight=9)
