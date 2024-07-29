import argon2

from argon2 import PasswordHasher


# https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
# https://argon2-cffi.readthedocs.io/en/stable/api.html
password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=1,
    hash_len=32,
    salt_len=16,
    encoding='utf-8',
    type=argon2.low_level.Type.ID
)


def hash_password(plain_password):
    return password_hasher.hash(plain_password)


def verify_password(plain_password, verified_hash):
    return password_hasher.verify(verified_hash, plain_password)

