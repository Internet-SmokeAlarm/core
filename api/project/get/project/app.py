import json

from fmlaas import get_project_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.get_project import GetProjectController
from fmlaas.exception import RequestForbiddenException
from fmlaas import DecimalEncoder


def lambda_handler(event, context):
    req_json = event.get("pathParameters")
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        project_id = id_processor.get_project_id()

        auth_context = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }

    dynamodb_ = DynamoDBInterface(get_project_table_name_from_env())

    try:
        project_json = GetProjectController(dynamodb_,
                                            project_id,
                                            auth_context).execute()

        return {
            "statusCode": 200,
            "body": json.dumps(project_json, cls=DecimalEncoder)
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "body": json.dumps({"error_msg": str(error)})
        }
