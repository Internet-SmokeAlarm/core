import json

from fmlaas.request_processor import IDProcessor
from fmlaas import get_job_table_name_from_env
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.exception import RequestForbiddenException
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.submit_job_start_model import submit_job_start_model_controller

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        job_id = id_processor.get_job_id()

        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : json.dumps({"error_msg" : str(error)})
        }

    group_db = DynamoDBInterface(get_group_table_name_from_env())
    job_db = DynamoDBInterface(get_job_table_name_from_env())

    try:
        can_submit_start_model, presigned_url = submit_job_start_model_controller(group_db,
                                                                                    job_db,
                                                                                    job_id,
                                                                                    auth_context_processor)

        if not can_submit_start_model:
            return {
                "statusCode" : 400,
                "body" : json.dumps({"error_msg" : "Cannot submit model to this job because it is not in initialization state"})
            }
        else:
            return {
                "statusCode" : 200,
                "body" : json.dumps({"model_url" : presigned_url})
            }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 403,
            "body" : json.dumps({"error_msg" : str(error)})
        }
