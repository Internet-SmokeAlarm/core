import json

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

    return {
        "statusCode" : 200,
        "body" : json.dumps({"model_url" : presigned_url})
    }
