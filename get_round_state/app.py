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
        round_id = id_processor.get_round_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    group = FLGroup.load_from_db(group_id, dynamodb_)

    if group.contains_round(round_id):
        round_json = group.get_round(round_id).to_json()

        simplified_round_json = {
            "ID" : round_json["ID"],
            "status" : round_json["status"],
            "previous_round_id" : round_json["previous_round_id"]
        }

        return {
            "statusCode" : 200,
            "body" : json.dumps(simplified_round_json)
        }
    else:
        return {
            "statusCode" : 400,
            "body" : "Round does not exist."
        }
