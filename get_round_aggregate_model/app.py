import json

from fmlaas import get_round_table_name_from_env
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.controller.get_round_aggregate_model import get_round_aggregate_model_controller

def lambda_handler(event, context):
    req_json = event.get("pathParameters")
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
        round_id = id_processor.get_round_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    group_db = DynamoDBInterface(get_group_table_name_from_env())
    round_db = DynamoDBInterface(get_round_table_name_from_env())

    is_round_complete, presigned_url = get_round_aggregate_model_controller(group_db,
                                                                            round_db,
                                                                            group_id,
                                                                            round_id,
                                                                            auth_json)

    if is_round_complete:
        return {
            "statusCode" : 200,
            "body" : json.dumps({"model_url" : presigned_url})
        }
    else:
        return {
            "statusCode" : 400,
            "body" : "Cannot get aggregate model for incomplete round"
        }
