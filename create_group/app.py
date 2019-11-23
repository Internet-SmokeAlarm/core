import json

from fmlaas import generate_unique_id
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    group_name = req_json["group_name"]

    # TODO : Authenticate user

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())

    group_id = generate_unique_id()
    group = FLGroup(group_name, id=group_id, devices=[], rounds=[])

    FLGroup.save_to_db(group, dynamodb_)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"group_id" : group_id})
    }
