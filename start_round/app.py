import json

from fmlaas import get_round_table_name_from_env
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import RoundConfiguration
from fmlaas.controllers.start_round import start_round_controller
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

    round_db = DynamoDBInterface(get_round_table_name_from_env())
    group_db = DynamoDBInterface(get_group_table_name_from_env())

    round_config = RoundConfiguration(num_devices, device_selection_strategy)

    round_id = start_round_controller(round_db, group_db, group_id, round_config)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"round_id" : round_id})
    }
