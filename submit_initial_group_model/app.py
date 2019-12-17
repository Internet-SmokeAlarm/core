import json

from fmlaas import generate_device_key_pair
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas.aws import create_presigned_post
from fmlaas.aws import get_models_bucket_name
from fmlaas import HierarchicalModelNameStructure

EXPIRATION_SEC = 60 * 30
FIELDS = {}
CONDITIONS = []

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    group_id = str(req_json["group_id"])

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    group = FLGroup.load_from_db(group_id, dynamodb_)

    model_name = HierarchicalModelNameStructure()
    model_name.generate_name(group_id=group_id)

    presigned_url = create_presigned_post(get_models_bucket_name(), model_name.get_name(),
                                          FIELDS, CONDITIONS, expiration=EXPIRATION_SEC)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"model_url" : presigned_url})
    }
