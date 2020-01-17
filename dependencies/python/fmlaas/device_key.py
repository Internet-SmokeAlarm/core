from uuid import uuid4

from .generate_unique_id import generate_unique_id
from .generate_unique_id import generate_partial_unique_id

def generate_device_key_pair():
    """
    Generates unique device key pair.

    Returns the device ID (16 characters) followed by the device API key (32 characters)
    """
    return generate_partial_unique_id(), generate_unique_id()
