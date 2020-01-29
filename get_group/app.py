import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.controller.get_group import get_group_controller
from fmlaas.exception import RequestForbiddenException

def lambda_handler(event, context):
    req_json = event.get("pathParameters")
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())

    try:
        group_json = get_group_controller(dynamodb_, group_id, auth_json)

        return {
            "statusCode" : 200,
            "body" : json.dumps(group_json)
        }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 401,
            "body" : str(error)
        }
