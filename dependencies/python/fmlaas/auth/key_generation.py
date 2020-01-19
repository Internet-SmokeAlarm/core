import secrets
from .auth_constants import AuthConstants

def generate_secret():
    return secrets.token_urlsafe(AuthConstants.SECRET_BYTE_SIZE)
