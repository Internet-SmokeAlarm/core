import boto3


def trigger_lambda_function(function_name, payload):
    """
    :param function_name: string
    :param payload: string
    """
    client = boto3.client('lambda')
    client.invoke(
        FunctionName=function_name,
        InvocationType="Event",
        Payload=payload)
