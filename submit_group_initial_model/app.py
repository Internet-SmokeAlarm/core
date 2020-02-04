import json

from fmlaas.aws import create_presigned_post
from fmlaas.aws import get_models_bucket_name
from fmlaas import HierarchicalModelNameStructure
from fmlaas.request_processor import IDProcessor
from fmlaas.exception import RequestForbiddenException
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.controller.submit_group_initial_model import submit_group_initial_model_controller

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    group_db = DynamoDBInterface(get_group_table_name_from_env())

    try:
        presigned_url = submit_group_initial_model_controller(group_db, group_id, auth_json)

        return {
            "statusCode" : 200,
            "body" : json.dumps({"model_url" : presigned_url})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 403,
            "body" : str(error)
        }
