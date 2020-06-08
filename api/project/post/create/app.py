import json

from fmlaas import get_project_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.create_project import CreateProjectController
from fmlaas.exception import RequestForbiddenException


def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        project_name = id_processor.get_project_name()

        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }

    dynamodb_ = DynamoDBInterface(get_project_table_name_from_env())

    try:
        project_id = CreateProjectController(dynamodb_,
                                             project_name,
                                             auth_context_processor).execute()

        return {
            "statusCode": 200,
            "body": json.dumps({"project_id": project_id})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "body": json.dumps({"error_msg": str(error)})
        }
