import secrets
from .auth_constants import AuthConstants


def generate_secret():
    return secrets.token_hex(AuthConstants.SECRET_BYTE_SIZE)


def generate_key_pair():
    secret = generate_secret()
    id = secret[:AuthConstants.ID_NUM_CHARS]

    return id, secret


def get_id_from_token(token):
    return token[:AuthConstants.ID_NUM_CHARS]
