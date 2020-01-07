import json

from fmlaas import get_round_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import DBObject
from fmlaas.model import Round
from fmlaas.request_processor import IDProcessor

def lambda_handler(event, context):
    req_json = event.get("pathParameters")

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
        dynamodb_ = DynamoDBInterface(get_round_table_name_from_env())
        round = DBObject.load_from_db(Round, round_id, dynamodb_)
    except KeyError:
        return {
            "statusCode" : 400,
            "body" : "Round does not exist"
        }

    is_device_active = round.is_device_active(device_id)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"is_device_active" : is_device_active})
    }
