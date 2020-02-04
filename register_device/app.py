import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas import get_auth_key_table_from_env
from fmlaas.controller.register_device import register_device_controller
from fmlaas.exception import RequestForbiddenException

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    group_db = DynamoDBInterface(get_group_table_name_from_env())
    key_db = DynamoDBInterface(get_auth_key_table_from_env())

    try:
        id, key_plaintext = register_device_controller(group_db, key_db, group_id, auth_json)

        return {
            "statusCode" : 200,
            "body" : json.dumps({"device_id" : id, "device_api_key" : key_plaintext})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 403,
            "body" : str(error)
        }
