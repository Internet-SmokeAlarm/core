import json

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
        print("TESTING")
        id_processor = IDProcessor(req_json)
        project_id = id_processor.get_project_id()
        experiment_id = id_processor.get_experiment_id()
        num_jobs = id_processor.get_num_jobs()

        print("TESTING 1")

        job_config_processor = JobConfigJSONProcessor(req_json)
        job_config = job_config_processor.generate_job_config()

        print("TESTING 2")

        auth_context = AuthContextProcessor(auth_json)

        print("TESTING 3")

        project_db = DynamoDBInterface(get_project_table_name_from_env())

        jobs = StartJobController(project_db,
                                  project_id,
                                  experiment_id,
                                  num_jobs,
                                  job_config,
                                  auth_context).execute()

        print("TESTING 4")
        print(jobs)

        return {
            "statusCode": 200,
            "body": json.dumps([job.to_json() for job in jobs])
        }
    except ValueError as error:
        print(f"VALUE ERROR: {str(error)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "body": json.dumps({"error_msg": str(error)})
        }
