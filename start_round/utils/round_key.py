from uuid import uuid4

def generate_round_key():
    """
    Generates unique round key.

    Returns the device ID (64 bits)
    """
    return uuid4().int >> 64
