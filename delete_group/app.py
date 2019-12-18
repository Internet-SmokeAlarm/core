import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import RequestJSONProcessor

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    try:
        req_json_processor = RequestJSONProcessor(req_json)
        group_id = req_json_processor.get_group_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    success = dynamodb_.delete_object(group_id)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"success" : success})
    }
