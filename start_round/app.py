import json

from fmlaas import get_round_table_name_from_env
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.controller.start_round import start_round_controller
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.request_processor import RoundConfigJSONProcessor
from fmlaas.exception import RequestForbiddenException

def lambda_handler(event, context):
    """
    {
        "group_id" : "group id",
        "device_selection_strategy" : "device selection strategy",
        "num_devices" : int_number_of_devices,
        "termination_criteria" : [
            {
                "type" : "Duration",
                "max_duration" : int_max_number_of_seconds
            }
        ]
    }
    """
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()

        round_config_processor = RoundConfigJSONProcessor(req_json)
        round_config = round_config_processor.generate_round_config()

        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    round_db = DynamoDBInterface(get_round_table_name_from_env())
    group_db = DynamoDBInterface(get_group_table_name_from_env())

    try:
        round_id = start_round_controller(round_db,
                                          group_db,
                                          group_id,
                                          round_config,
                                          auth_context_processor)

        return {
            "statusCode" : 200,
            "body" : json.dumps({"round_id" : round_id})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 403,
            "body" : str(error)
        }
