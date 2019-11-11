import json

from fmlaas import get_group_table_name_from_env
from fmlaas import DynamoDBInterface
from fmlaas import FLGroup
from fmlaas import create_presigned_post
from fmlaas import generate_model_object_name
from fmlaas import get_models_bucket_name

EXPIRATION_SEC = 60 * 30
FIELDS = {}
CONDITIONS = []

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    group_id = req_json["group_id"]
    round_id = req_json["round_id"]
    device_id = req_json["device_id"]

    # TODO : Authenticate user

    model_object_name = generate_model_object_name(device_id, round_id)
    presigned_url = create_presigned_post(get_models_bucket_name(), model_object_name,
                                          FIELDS, CONDITIONS, expiration=EXPIRATION_SEC)

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    group = FLGroup.load_from_db(group_id, dynamodb_)

    group.add_model_to_round(round_id, model_object_name)

    FLGroup.save_to_db(group, dynamodb_)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"model_url" : presigned_url})
    }
