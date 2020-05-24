import json

from fmlaas import get_group_table_name_from_env
from fmlaas import get_job_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.get_job import get_job_controller
from fmlaas.exception import RequestForbiddenException


def lambda_handler(event, context):
    req_json = event.get("pathParameters")
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
        job_id = id_processor.get_job_id()

        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }

    try:
        group_db_ = DynamoDBInterface(get_group_table_name_from_env())
        job_db_ = DynamoDBInterface(get_job_table_name_from_env())

        job = get_job_controller(group_db_,
                                 job_db_,
                                 group_id,
                                 job_id,
                                 auth_context_processor)

        # TODO : Need to remove unnecessary content from return JSON.
        #   Should probably happen inside the controller.

        return {
            "statusCode": 200,
            "body": json.dumps(job.to_json())
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "body": json.dumps({"error_msg": str(error)})
        }
