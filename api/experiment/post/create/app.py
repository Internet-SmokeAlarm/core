import json

from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import ExperimentConfigProcessor
from fmlaas import get_project_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.exception import RequestForbiddenException
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.create_experiment import CreateExperimentController
from fmlaas.utils import get_allowed_origins


def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        project_id = id_processor.get_project_id()
        experiment_name = id_processor.get_experiment_name()
        experiment_description = id_processor.get_experiment_description()

        experiment_config_processor = ExperimentConfigProcessor(req_json)
        experiment_config = experiment_config_processor.generate_experiment_config()

        auth_context = AuthContextProcessor(auth_json)

        project_db = DynamoDBInterface(get_project_table_name_from_env())

        experiment = CreateExperimentController(project_db,
                                                project_id,
                                                experiment_name,
                                                experiment_description,
                                                experiment_config,
                                                auth_context).execute()

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps(experiment.to_json())
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
