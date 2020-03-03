import json

from fmlaas import get_round_table_name_from_env
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.exception import RequestForbiddenException
from fmlaas.controller.is_device_active import is_device_active_controller

def lambda_handler(event, context):
    req_json = event.get("pathParameters")
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
        round_id = id_processor.get_round_id()
        device_id = id_processor.get_device_id()

        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    group_db = DynamoDBInterface(get_group_table_name_from_env())
    round_db = DynamoDBInterface(get_round_table_name_from_env())

    try:
        is_device_active = is_device_active_controller(group_db,
                                                       round_db,
                                                       group_id,
                                                       round_id,
                                                       device_id,
                                                       auth_context_processor)

        return {
            "statusCode" : 200,
            "body" : json.dumps({"is_device_active" : is_device_active})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 403,
            "body" : str(error)
        }
