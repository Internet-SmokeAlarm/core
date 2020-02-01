import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.exception import RequestForbiddenException
from fmlaas.controller.get_group_initial_model import get_group_initial_model_controller

def lambda_handler(event, context):
    req_json = event.get("pathParameters")
    auth_json = event["requestContext"]["authorizer"]

    EXPIRATION_SEC = 60 * 5

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
        is_initial_model_set, presigned_url = get_group_initial_model_controller(dynamodb_, group_id, auth_json)

        if is_initial_model_set:
            return {
                "statusCode" : 200,
                "body" : json.dumps({"model_url" : presigned_url})
            }
        else:
            return {
                "statusCode" : 500,
                "body" : "Initial model not set for group"
            }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 401,
            "body" : str(error)
        }
