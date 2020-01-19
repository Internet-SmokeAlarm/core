import secrets
from .auth_constants import AuthConstants

def generate_secret():
    return secrets.token_urlsafe(AuthConstants.SECRET_BYTE_SIZE)

def generate_key_pair():
    secret = generate_secret()
    id = secret[:24]

    return id, secret
