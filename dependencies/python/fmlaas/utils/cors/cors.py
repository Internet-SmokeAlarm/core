def get_allowed_origins() -> str:
    """
    NOTE: According to AWS, API GW only allows one value in the allowed origins
    header.
    """
    return "*"
