import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas.model import RoundConfiguration
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import RoundConfigJSONProcessor

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()

        round_config_processor = RoundConfigJSONProcessor(req_json)
        num_devices = round_config_processor.get_num_devices()
        device_selection_strategy = round_config_processor.get_device_selection_strategy()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    group = FLGroup.load_from_db(group_id, dynamodb_)

    round_config = RoundConfiguration(num_devices, device_selection_strategy)
    round_id = group.create_round(round_config)

    group.save_to_db(dynamodb_)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"round_id" : round_id})
    }
