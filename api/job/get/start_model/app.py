import json

from fmlaas import get_job_table_name_from_env
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.exception import RequestForbiddenException
from fmlaas.controller.get_job_start_model import GetJobStartModelController


def lambda_handler(event, context):
    req_json = event.get("pathParameters")
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        job_id = id_processor.get_job_id()

        auth_context = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }

    group_db = DynamoDBInterface(get_group_table_name_from_env())
    job_db = DynamoDBInterface(get_job_table_name_from_env())

    try:
        presigned_url = GetJobStartModelController(group_db,
                                                   job_db,
                                                   job_id,
                                                   auth_context).execute()
        return {
            "statusCode": 200,
            "body": json.dumps({"model_url": presigned_url})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "body": json.dumps({"error_msg": str(error)})
        }
