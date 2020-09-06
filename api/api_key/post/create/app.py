import json

from fmlaas import get_auth_key_table_from_env
from fmlaas import get_user_table_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.exception import RequestForbiddenException
from fmlaas.controller.create_api_key import CreateApiKeyController
from fmlaas.utils import get_allowed_origins


def lambda_handler(event, context):
    auth_json = event["requestContext"]["authorizer"]

    try:
        auth_context = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps({"error_msg": str(error)})
        }

    api_key_db = DynamoDBInterface(get_auth_key_table_from_env())
    user_db = DynamoDBInterface(get_user_table_from_env())

    try:
        key_plaintext = CreateApiKeyController(api_key_db,
                                               user_db,
                                               auth_context).execute()

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps({"key": key_plaintext})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps({"error_msg": str(error)})
        }
