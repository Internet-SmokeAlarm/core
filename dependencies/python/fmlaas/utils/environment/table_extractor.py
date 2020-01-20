import os

def get_group_table_name_from_env():
    return os.environ["GROUPS_TABLE_NAME"]

def get_round_table_name_from_env():
    return os.environ["ROUNDS_TABLE_NAME"]

def get_auth_key_table_from_env():
    return os.environ["AUTH_KEY_TABLE_NAME"]
