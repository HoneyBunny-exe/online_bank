import secrets
import hashlib
import config


def calculate_password_hash(row_password: str, salt: str = None):
    if salt is None:
        salt = secrets.token_bytes(16)
    else:
        salt = bytes.fromhex(salt)
    password_hash = hashlib.scrypt(row_password.encode(), salt=salt, n=16384, r=8, p=1, dklen=32)
    return password_hash.hex(), salt.hex()


def compare_passwords(password_hash: str, salt: str, row_password: str):
    new_hash, _ = calculate_password_hash(row_password, salt)
    a = bytes.fromhex(password_hash)
    b = bytes.fromhex(new_hash)
    return secrets.compare_digest(a, b)


def compare_digest(hash_a, hash_b):
    a = bytes.fromhex(hash_a)
    b = bytes.fromhex(hash_b)
    return secrets.compare_digest(a, b)


def create_auth_token(unique_string: str):
    salt = secrets.token_bytes(16)
    token = hashlib.pbkdf2_hmac('sha256', unique_string.encode(), salt, 2048, dklen=32)
    return token.hex()


def create_confirm_code():
    code = [str(secrets.randbelow(10)) for _ in range(config.LENGTH_CONFIRM_CODE)]
    return ''.join(code)

