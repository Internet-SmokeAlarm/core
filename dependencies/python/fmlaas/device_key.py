from uuid import uuid4

def generate_device_key_pair():
    """
    Generates unique device key pair.

    Returns the device ID (64 bits) followed by the device API key (128 bits)
    """
    device_id = int(str(uuid4().int >> 64)[:16])
    device_api_key = str(uuid4())

    return device_id, device_api_key
