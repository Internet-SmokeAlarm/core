import json

from fmlaas.request_processor import IDProcessor
from fmlaas import get_round_table_name_from_env
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.exception import RequestForbiddenException
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.submit_round_start_model import submit_round_start_model_controller

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        round_id = id_processor.get_round_id()

        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    group_db = DynamoDBInterface(get_group_table_name_from_env())
    round_db = DynamoDBInterface(get_round_table_name_from_env())

    try:
        can_submit_start_model, presigned_url = submit_round_start_model_controller(group_db,
                                                                                    round_db,
                                                                                    round_id,
                                                                                    auth_context_processor)

        if not can_submit_start_model:
            return {
                "statusCode" : 400,
                "body" : "Cannot submit model to this round because it is not in initialization state"
            }
        else:
            return {
                "statusCode" : 200,
                "body" : json.dumps({"model_url" : presigned_url})
            }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 403,
            "body" : str(error)
        }
