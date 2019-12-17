import json

from fmlaas.aws import create_presigned_post
from fmlaas import HierarchicalModelNameStructure
from fmlaas.aws import get_models_bucket_name
from fmlaas.request_processor import RequestJSONProcessor

EXPIRATION_SEC = 60 * 30
FIELDS = {}
CONDITIONS = []

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    try:
        req_json_processor = RequestJSONProcessor(req_json)
        group_id = req_json_processor.get_group_id()
        round_id = req_json_processor.get_round_id()
        device_id = req_json_processor.get_device_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    object_name = HierarchicalModelNameStructure()
    object_name.generate_name(group_id, round_id, device_id)
    presigned_url = create_presigned_post(get_models_bucket_name(), object_name.get_name(),
                                          FIELDS, CONDITIONS, expiration=EXPIRATION_SEC)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"model_url" : presigned_url})
    }
