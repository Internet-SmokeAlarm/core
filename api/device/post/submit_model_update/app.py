import json

from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas import get_job_table_name_from_env
from fmlaas import get_project_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.exception import RequestForbiddenException
from fmlaas.controller.submit_model_update import SubmitModelUpdateController
from fmlaas.utils import get_allowed_origins


def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        project_id = id_processor.get_project_id()
        job_id = id_processor.get_job_id()

        auth_context = AuthContextProcessor(auth_json)

        project_db = DynamoDBInterface(get_project_table_name_from_env())
        job_db = DynamoDBInterface(get_job_table_name_from_env())

        can_submit_model_to_job, presigned_url = SubmitModelUpdateController(project_db,
                                                                             job_db,
                                                                             project_id,
                                                                             job_id,
                                                                             auth_context).execute()

        if not can_submit_model_to_job:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": get_allowed_origins()
                },
                "body": json.dumps({"error_msg": "Cannot submit model to this job. Either device is not active, or job is complete"})
            }
        else:
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": get_allowed_origins()
                },
                "body": json.dumps({"model_url": presigned_url})
            }
    except ValueError as error:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps({"error_msg": str(error)})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps({"error_msg": str(error)})
        }
