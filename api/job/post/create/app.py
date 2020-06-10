import json

from fmlaas import get_job_table_name_from_env
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.controller.start_job import start_job_controller
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.request_processor import JobConfigJSONProcessor
from fmlaas.exception import RequestForbiddenException


def lambda_handler(event, context):
    """
    {
        "group_id" : "group id",
        "device_selection_strategy" : "device selection strategy",
        "num_devices" : int_number_of_devices,
        "num_buffer_devices" int_number_of_buffer_devices,
        "previous_job_id" : "previous job id",
        "termination_criteria" : [
            {
                "type" : "Duration",
                "max_duration" : int_max_number_of_seconds
            }
        ]
    }
    """
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
        previous_job_id = id_processor.get_previous_job_id()

        job_config_processor = JobConfigJSONProcessor(req_json)
        job_config = job_config_processor.generate_job_config()

        auth_context = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }

    job_db = DynamoDBInterface(get_job_table_name_from_env())
    group_db = DynamoDBInterface(get_group_table_name_from_env())

    try:
        job_id = start_job_controller(job_db,
                                      group_db,
                                      group_id,
                                      job_config,
                                      previous_job_id,
                                      auth_context)

        return {
            "statusCode": 200,
            "body": json.dumps({"job_id": job_id})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "body": json.dumps({"error_msg": str(error)})
        }
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }
