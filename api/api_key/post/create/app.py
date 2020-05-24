import json

from fmlaas import get_auth_key_table_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.exception import RequestForbiddenException
from fmlaas.controller.create_api_key import create_api_key_controller


def lambda_handler(event, context):
    auth_json = event["requestContext"]["authorizer"]

    try:
        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }

    dynamodb_ = DynamoDBInterface(get_auth_key_table_from_env())

    try:
        key_plaintext = create_api_key_controller(
            dynamodb_, auth_context_processor)

        return {
            "statusCode": 200,
            "body": json.dumps({"key": key_plaintext})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "body": json.dumps({"error_msg": str(error)})
        }
