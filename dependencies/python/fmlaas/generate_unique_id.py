from uuid import uuid4

def generate_unique_id():
    return str(uuid4().int >> 64)[:16]
