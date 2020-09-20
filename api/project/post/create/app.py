import json

from fmlaas import get_project_table_name_from_env
from fmlaas import get_user_table_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.create_project import CreateProjectController
from fmlaas.exception import RequestForbiddenException
from fmlaas.utils import get_allowed_origins


def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        project_name = id_processor.get_project_name()
        project_description = id_processor.get_project_description()

        auth_context = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps({"error_msg": str(error)})
        }

    project_db = DynamoDBInterface(get_project_table_name_from_env())
    user_db = DynamoDBInterface(get_user_table_from_env())

    try:
        project = CreateProjectController(project_db,
                                          user_db,
                                          project_name,
                                          project_description,
                                          auth_context).execute()

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps(project.to_json())
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "headers": {
                "Access-Control-Allow-Origin": get_allowed_origins()
            },
            "body": json.dumps({"error_msg": str(error)})
        }
