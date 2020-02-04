import json

from fmlaas.request_processor import IDProcessor
from fmlaas import get_round_table_name_from_env
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.exception import RequestForbiddenException
from fmlaas.controller.submit_model_update import submit_model_update_controller

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
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

    try:
        can_submit_model_to_round, presigned_url = submit_model_update_controller(group_db, round_db, group_id, round_id, auth_json)

        if not can_submit_model_to_round:
            return {
                "statusCode" : 400,
                "body" : "Cannot submit model to this round. Either device is not active, or round is complete"
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
