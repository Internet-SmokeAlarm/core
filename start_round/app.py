import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas.model import RoundConfiguration
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
    group = FLGroup.load_from_db(group_id, dynamodb_)

    # TODO : Handle round configuration that is passed
    round_config = RoundConfiguration(str(len(group.get_device_list())))
    round_id = group.create_round(round_config)

    group.save_to_db(dynamodb_)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"round_id" : round_id})
    }
