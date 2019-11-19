from uuid import uuid4

from .generate_unique_id import generate_unique_id

def generate_device_key_pair():
    """
    Generates unique device key pair.

    Returns the device ID (64 bits) followed by the device API key (128 bits)
    """
    device_api_key = str(uuid4())

    return generate_unique_id(), device_api_key
