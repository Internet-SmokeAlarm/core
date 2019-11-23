import json

from fmlaas import generate_device_key_pair
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas.aws import create_presigned_url
from fmlaas.aws import get_models_bucket_name

EXPIRATION_SEC = 60 * 5

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    group_id = req_json["group_id"]
    round_id = req_json["round_id"]

    # TODO : Authenticate user

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    group = FLGroup.load_from_db(group_id, dynamodb_)

    object_name = group.get_round_aggregate_model(round_id)

    presigned_url = create_presigned_url(get_models_bucket_name(), object_name, expiration=EXPIRATION_SEC)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"model_url" : presigned_url})
    }
