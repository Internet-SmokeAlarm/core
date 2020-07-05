import json

from fmlaas import get_project_table_name_from_env
from fmlaas import get_job_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.get_job import GetJobController
from fmlaas.exception import RequestForbiddenException


def lambda_handler(event, context):
    req_json = event.get("pathParameters")
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        project_id = id_processor.get_project_id()
        job_id = id_processor.get_job_id()

        auth_context = AuthContextProcessor(auth_json)

        project_db = DynamoDBInterface(get_project_table_name_from_env())
        job_db = DynamoDBInterface(get_job_table_name_from_env())

        job = GetJobController(project_db,
                               job_db,
                               project_id,
                               job_id,
                               auth_context).execute()

        # TODO : Need to remove unnecessary content from return JSON.
        #   Should probably happen inside the controller.

        return {
            "statusCode": 200,
            "body": json.dumps(job.to_json())
        }
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "body": json.dumps({"error_msg": str(error)})
        }
