import json

from fmlaas.request_processor import IDProcessor
from fmlaas import get_project_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.exception import RequestForbiddenException
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.get_experiment import GetExperimentController


def lambda_handler(event, context):
    req_json = event.get("pathParameters")
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        project_id = id_processor.get_project_id()
        experiment_id = id_processor.get_experiment_id()

        auth_context = AuthContextProcessor(auth_json)

        project_db = DynamoDBInterface(get_project_table_name_from_env())

        experiment = GetExperimentController(project_db,
                                             project_id,
                                             experiment_id,
                                             auth_context).execute()

        return {
            "statusCode": 200,
            "body": json.dumps(experiment.to_json())
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
