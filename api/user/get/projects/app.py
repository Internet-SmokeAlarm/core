import json

from fmlaas import get_user_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.user.get import GetProjectsController
from fmlaas.exception import RequestForbiddenException
from fmlaas.utils import get_allowed_origins


def lambda_handler(event, context):
    req_json = event.get("pathParameters")
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

    db = DynamoDBInterface(get_user_table_name_from_env())

    try:
        projects = GetProjectsController(db,
                                         auth_context).execute()

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps(projects)
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps({"error_msg": str(error)})
        }
