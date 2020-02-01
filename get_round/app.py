import json

from fmlaas import get_group_table_name_from_env
from fmlaas import get_round_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.controller.get_round import get_round_controller
from fmlaas.exception import RequestForbiddenException

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

    try:
        group_db_ = DynamoDBInterface(get_group_table_name_from_env())
        round_db_ = DynamoDBInterface(get_round_table_name_from_env())

        round = get_round_controller(group_db_, round_db_, group_id, round_id, auth_json)

        return {
            "statusCode" : 200,
            "body" : json.dumps(round.to_json())
        }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 401,
            "body" : str(error)
        }
