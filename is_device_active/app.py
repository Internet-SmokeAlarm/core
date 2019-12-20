import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas.request_processor import IDProcessor

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
        device_id = id_processor.get_device_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    try:
        dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
        group = FLGroup.load_from_db(group_id, dynamodb_)
    except KeyError:
        return {
            "statusCode" : 403,
            "body" : "Group does not exist or you are not authorized to access it."
        }

    is_device_active = group.is_device_active(device_id)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"is_device_active" : is_device_active})
    }
