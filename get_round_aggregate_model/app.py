import json

from fmlaas import generate_device_key_pair
from fmlaas import get_round_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import Round
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
        round_id = id_processor.get_round_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    try:
        dynamodb_ = DynamoDBInterface(get_round_table_name_from_env())
        round = DBObject.load_from_db(Round, round_id, dynamodb_)
    except KeyError:
        return {
            "statusCode" : 400,
            "body" : "Round does not exist"
        }

    if round.is_complete():
        object_name = round.get_aggregate_model().get_name().get_name()

        presigned_url = create_presigned_url(get_models_bucket_name(), object_name, expiration=EXPIRATION_SEC)

        return {
            "statusCode" : 200,
            "body" : json.dumps({"model_url" : presigned_url})
        }
    else:
        return {
            "statusCode" : 400,
            "body" : "Cannot get aggregate model for incomplete round"
        }
