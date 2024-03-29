import json

from fmlaas import get_project_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas import get_auth_key_table_from_env
from fmlaas.controller.register_device import RegisterDeviceController
from fmlaas.exception import RequestForbiddenException


def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        project_id = id_processor.get_project_id()

        auth_context = AuthContextProcessor(auth_json)

        project_db = DynamoDBInterface(get_project_table_name_from_env())
        key_db = DynamoDBInterface(get_auth_key_table_from_env())

        id, key_plaintext = RegisterDeviceController(project_db,
                                                     key_db,
                                                     project_id,
                                                     auth_context).execute()

        return {
            "statusCode": 200,
            "body": json.dumps({"device_id": id, "device_api_key": key_plaintext})
        }
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "body": json.dumps({"error_msg": str(error)})
        }
