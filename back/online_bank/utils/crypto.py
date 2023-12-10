import hashlib
import secrets

secret_key = secrets.token_bytes(32)


def mul_x(polynomial):
    high_bit = polynomial & 0x80
    shl = (polynomial << 1) & 0xff
    return shl if high_bit == 0 else shl ^ 0x1b


class BaseEncrypt:
    ...


def exec_k(n):
    arr = list()
    for i in range(0, n):
        a = list()
        for z in range(0, i+1):
            for j in range(0, i+1):
                a.append(f'b_{z}a_{j}')
        arr.append(a)
    return arr

