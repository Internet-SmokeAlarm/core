import json

from fmlaas.aws import create_presigned_post
from fmlaas import HierarchicalModelNameStructure
from fmlaas.aws import get_models_bucket_name

EXPIRATION_SEC = 60 * 30
FIELDS = {}
CONDITIONS = []

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    group_id = str(req_json["group_id"])
    round_id = str(req_json["round_id"])
    device_id = str(req_json["device_id"])

    object_name = HierarchicalModelNameStructure()
    object_name.generate_name(group_id, round_id, device_id)
    presigned_url = create_presigned_post(get_models_bucket_name(), object_name.get_name(),
                                          FIELDS, CONDITIONS, expiration=EXPIRATION_SEC)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"model_url" : presigned_url})
    }
