from uuid import uuid4

def generate_group_id():
    """
    Generates a unique group key.

    Returns the group ID (64 bits)
    """
    return uuid4().int >> 64
