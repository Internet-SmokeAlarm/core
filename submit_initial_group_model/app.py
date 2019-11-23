import json

from fmlaas import generate_device_key_pair
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas.aws import create_presigned_post
from fmlaas.aws import get_models_bucket_name

EXPIRATION_SEC = 60 * 30
FIELDS = {}
CONDITIONS = []

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    group_id = req_json["group_id"]

    # TODO : Authenticate user

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    group = FLGroup.load_from_db(group_id, dynamodb_)

    group_initial_model_name = group.get_initial_model()

    presigned_url = create_presigned_post(get_models_bucket_name(), group_initial_model_name,
                                          FIELDS, CONDITIONS, expiration=EXPIRATION_SEC)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"model_url" : presigned_url})
    }
