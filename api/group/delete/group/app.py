import json

from fmlaas import get_group_table_name_from_env
from fmlaas import get_round_table_name_from_env
from fmlaas.aws import delete_s3_objects_with_prefix
from fmlaas.aws import get_models_bucket_name
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.exception import RequestForbiddenException
from fmlaas.controller.delete_group import delete_group_controller

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()

        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : json.dumps({"error_msg" : str(error)})
        }

    group_db = DynamoDBInterface(get_group_table_name_from_env())
    round_db = DynamoDBInterface(get_round_table_name_from_env())

    try:
        delete_group_controller(group_db,
                                round_db,
                                group_id,
                                auth_context_processor)
        delete_s3_objects_with_prefix(get_models_bucket_name(), group_id)

        return {
            "statusCode" : 200,
            "body" : "{}"
        }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 403,
            "body" : json.dumps({"error_msg" : str(error)})
        }
