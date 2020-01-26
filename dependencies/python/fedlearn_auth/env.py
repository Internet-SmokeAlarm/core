import os

def get_userpool_id_from_env():
    return os.environ["COGNITO_USER_POOL_ID"]

def get_app_client_id_from_env():
    return os.environ["COGNITO_USER_POOL_CLIENT_ID"]
