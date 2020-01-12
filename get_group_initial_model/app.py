import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas.model import DBObject
from fmlaas.aws import create_presigned_url
from fmlaas.aws import get_models_bucket_name
from fmlaas.request_processor import IDProcessor

def lambda_handler(event, context):
    req_json = event.get("pathParameters")

    EXPIRATION_SEC = 60 * 5

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    group = DBObject.load_from_db(FLGroup, group_id, dynamodb_)

    presigned_url = create_presigned_url(
        get_models_bucket_name(),
        group.get_initial_model().get_name().get_name(),
        expiration=EXPIRATION_SEC)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"model_url" : presigned_url})
    }
