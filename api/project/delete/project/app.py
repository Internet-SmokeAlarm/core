import json

from fmlaas import get_project_table_name_from_env
from fmlaas import get_job_table_name_from_env
from fmlaas.aws import delete_s3_objects_with_prefix
from fmlaas.aws import get_models_bucket_name
from fmlaas.database import DynamoDBInterface
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import AuthContextProcessor
from fmlaas.exception import RequestForbiddenException
from fmlaas.controller.delete_project import DeleteProjectController


def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    auth_json = event["requestContext"]["authorizer"]

    try:
        id_processor = IDProcessor(req_json)
        project_id = id_processor.get_project_id()

        auth_context_processor = AuthContextProcessor(auth_json)
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": json.dumps({"error_msg": str(error)})
        }

    project_db = DynamoDBInterface(get_project_table_name_from_env())
    job_db = DynamoDBInterface(get_job_table_name_from_env())

    try:
        DeleteProjectController(project_db,
                                job_db,
                                project_id,
                                auth_context_processor).execute()
        delete_s3_objects_with_prefix(get_models_bucket_name(), project_id)

        return {
            "statusCode": 200,
            "body": "{}"
        }
    except RequestForbiddenException as error:
        return {
            "statusCode": 403,
            "body": json.dumps({"error_msg": str(error)})
        }
