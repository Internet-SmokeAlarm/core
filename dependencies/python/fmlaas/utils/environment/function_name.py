import os


def get_aggregation_lambda_func_name():
    return os.environ["AGGREGATION_LAMBDA_FUNCTION_NAME"]
