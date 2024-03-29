import json

from fmlaas import get_job_table_name_from_env
from fmlaas import get_project_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.controller.start_job import StartJobController
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.request_processor import JobConfigJSONProcessor
from fmlaas.exception import RequestForbiddenException


def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        project_id = id_processor.get_project_id()
        experiment_id = id_processor.get_experiment_id()

        job_config_processor = JobConfigJSONProcessor(req_json)
        job_config = job_config_processor.generate_job_config()

        auth_context = AuthContextProcessor(auth_json)

        job_db = DynamoDBInterface(get_job_table_name_from_env())
        project_db = DynamoDBInterface(get_project_table_name_from_env())

        job = StartJobController(job_db,
                                 project_db,
                                 project_id,
                                 experiment_id,
                                 job_config,
                                 auth_context).execute()

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
