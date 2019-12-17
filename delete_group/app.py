import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    group_id = req_json["group_id"]

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    success = dynamodb_.delete_object(group_id)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"success" : success})
    }
