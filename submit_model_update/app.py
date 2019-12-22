import json

from fmlaas.aws import create_presigned_post
from fmlaas import HierarchicalModelNameStructure
from fmlaas.aws import get_models_bucket_name
from fmlaas.request_processor import IDProcessor
from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    EXPIRATION_SEC = 60 * 10
    FIELDS = {}
    CONDITIONS = []

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()
        round_id = id_processor.get_round_id()
        device_id = id_processor.get_device_id()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    try:
        dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
        group = FLGroup.load_from_db(group_id, dynamodb_)
    except KeyError:
        return {
            "statusCode" : 400,
            "body" : "Group does not exist"
        }

    if not group.is_round_active(round_id) or not group.is_device_active(device_id):
        return {
            "statusCode" : 400,
            "body" : "Cannot submit model to this round. Either device is not active, or round is complete"
        }
    else:
        object_name = HierarchicalModelNameStructure()
        object_name.generate_name(group_id, round_id, device_id)

        presigned_url = create_presigned_post(
            get_models_bucket_name(),
            object_name.get_name(),
            FIELDS,
            CONDITIONS,
            expiration=EXPIRATION_SEC)

        return {
            "statusCode" : 200,
            "body" : json.dumps({"model_url" : presigned_url})
        }
