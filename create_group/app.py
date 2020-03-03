import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.controller.create_group import create_group_controller
from fmlaas.exception import RequestForbiddenException

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_name = id_processor.get_group_name()

        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())

    try:
        group_id = create_group_controller(dynamodb_,
                                           group_name,
                                           auth_context_processor)

        return {
            "statusCode" : 200,
            "body" : json.dumps({"group_id" : group_id})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 403,
            "body" : str(error)
        }
