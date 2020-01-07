import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas.model import DBObject
from fmlaas.request_processor import IDProcessor

def lambda_handler(event, context):
    req_json = event.get("pathParameters")

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    group = DBObject.load_from_db(FLGroup, group_id, dynamodb_)

    return {
        "statusCode" : 200,
        "body" : json.dumps(group.to_json())
    }
