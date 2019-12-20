import json

from fmlaas.aws import create_presigned_post
from fmlaas.aws import get_models_bucket_name
from fmlaas import HierarchicalModelNameStructure
from fmlaas.request_processor import IDProcessor

EXPIRATION_SEC = 60 * 30
FIELDS = {}
CONDITIONS = []

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    model_name = HierarchicalModelNameStructure()
    model_name.generate_name(group_id=group_id)

    presigned_url = create_presigned_post(get_models_bucket_name(), model_name.get_name(),
                                          FIELDS, CONDITIONS, expiration=EXPIRATION_SEC)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"model_url" : presigned_url})
    }
