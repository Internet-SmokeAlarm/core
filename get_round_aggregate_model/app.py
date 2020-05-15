import json

from fmlaas import get_round_table_name_from_env
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.get_round_aggregate_model import get_round_aggregate_model_controller
from fmlaas.exception import RequestForbiddenException

def lambda_handler(event, context):
    req_json = event.get("pathParameters")
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
        round_id = id_processor.get_round_id()

        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : json.dumps({"error_msg" : str(error)})
        }

    group_db = DynamoDBInterface(get_group_table_name_from_env())
    round_db = DynamoDBInterface(get_round_table_name_from_env())

    try:
        is_round_complete, presigned_url = get_round_aggregate_model_controller(group_db,
                                                                                round_db,
                                                                                group_id,
                                                                                round_id,
                                                                                auth_context_processor)

        if is_round_complete:
            return {
                "statusCode" : 200,
                "body" : json.dumps({"model_url" : presigned_url})
            }
        else:
            return {
                "statusCode" : 400,
                "body" : json.dumps({"error_msg" : "Cannot get aggregate model for incomplete round"})
            }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 403,
            "body" : json.dumps({"error_msg" : str(error)})
        }
