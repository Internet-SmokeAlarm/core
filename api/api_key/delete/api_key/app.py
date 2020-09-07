import json

from fmlaas import get_auth_key_table_from_env
from fmlaas import get_user_table_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.exception import RequestForbiddenException
from fmlaas.controller.delete_api_key import DeleteApiKeyController
from fmlaas.utils import get_allowed_origins


def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        auth_context = AuthContextProcessor(auth_json)

        id_processor = IDProcessor(req_json)
        key_to_remove = id_processor.get_api_key()
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
        DeleteApiKeyController(api_key_db,
                               user_db,
                               key_to_remove,
                               auth_context).execute()

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": "{}"
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps({"error_msg": str(error)})
        }
