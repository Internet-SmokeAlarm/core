import json

from fmlaas import generate_device_key_pair
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas.aws import create_presigned_url
from fmlaas.aws import get_models_bucket_name
from fmlaas.request_processor import IDProcessor

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

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

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    group = FLGroup.load_from_db(group_id, dynamodb_)

    if group.contains_round(round_id) and group.is_round_complete(round_id):
        object_name = group.get_round_aggregate_model(round_id).get_name().get_name()

        presigned_url = create_presigned_url(get_models_bucket_name(), object_name, expiration=EXPIRATION_SEC)

        return {
            "statusCode" : 200,
            "body" : json.dumps({"model_url" : presigned_url})
        }
    else:
        return {
            "statusCode" : 400,
            "body" : "Cannot get aggregate model for incomplete round or round that does not exist"
        }
