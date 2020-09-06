import os


def get_project_table_name_from_env():
    return os.environ["PROJECTS_TABLE_NAME"]


def get_job_table_name_from_env():
    return os.environ["JOBS_TABLE_NAME"]


def get_auth_key_table_from_env():
    return os.environ["AUTH_KEY_TABLE_NAME"]


def get_user_table_from_env():
    return os.environ["USERS_TABLE_NAME"]
