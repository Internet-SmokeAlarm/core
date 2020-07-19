import json

from fmlaas import get_job_table_name_from_env
from fmlaas import get_project_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.controller.testing_report import TestingReportController
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.request_processor import TestingReportProcessor
from fmlaas.exception import RequestForbiddenException


def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        job_id = id_processor.get_job_id()

        testing_report_processor = TestingReportProcessor(req_json)
        auth_context = AuthContextProcessor(auth_json)

        job_db = DynamoDBInterface(get_job_table_name_from_env())
        project_db = DynamoDBInterface(get_project_table_name_from_env())

        TestingReportController(job_db,
                                project_db,
                                job_id,
                                testing_report_processor,
                                auth_context).execute()

        return {
            "statusCode": 200,
            "body": "{}"
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
