import json

from fmlaas import get_group_table_name_from_env
from fmlaas import get_job_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.cancel_job import CancelJobController
from fmlaas.exception import RequestForbiddenException


def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
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
        CancelJobController(group_db,
                            job_db,
                            job_id,
                            auth_context).execute()

        return {
            "statusCode": 200,
            "body": "{}"
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "body": json.dumps({"error_msg": str(error)})
        }
    except Exception as error:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }
