import json

from fmlaas.request_processor import IDProcessor
from fmlaas import get_project_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.exception import RequestForbiddenException
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.submit_experiment_start_model import SubmitExperimentStartModelController
from fmlaas.utils import get_allowed_origins


def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        project_id = id_processor.get_project_id()
        experiment_id = id_processor.get_experiment_id()

        auth_context = AuthContextProcessor(auth_json)

        project_db = DynamoDBInterface(get_project_table_name_from_env())

        can_submit_start_model, presigned_url = SubmitExperimentStartModelController(project_db,
                                                                                     project_id,
                                                                                     experiment_id,
                                                                                     auth_context).execute()

        if not can_submit_start_model:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": get_allowed_origins()
                },
                "body": json.dumps({"error_msg": "Cannot submit model to this experiment because it is not in initialization state"})
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
