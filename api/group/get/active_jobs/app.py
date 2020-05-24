import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.get_group_current_job_id import get_group_current_job_id_controller
from fmlaas.exception import RequestForbiddenException

def lambda_handler(event, context):
    req_json = event.get("pathParameters")
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()

        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : json.dumps({"error_msg" : str(error)})
        }

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())

    try:
        current_job_ids = get_group_current_job_id_controller(dynamodb_,
                                                                 group_id,
                                                                 auth_context_processor)

        return {
            "statusCode" : 200,
            "body" : json.dumps({"job_ids" : current_job_ids})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 403,
            "body" : json.dumps({"error_msg" : str(error)})
        }
