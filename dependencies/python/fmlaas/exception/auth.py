class RequestForbiddenException(Exception):
    pass

def raise_default_request_forbidden_error():
    raise RequestForbiddenException("You are not authorized to access this resource")
