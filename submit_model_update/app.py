import json

from fmlaas.aws import create_presigned_post
from fmlaas import HierarchicalModelNameStructure
from fmlaas.aws import get_models_bucket_name
from fmlaas.request_processor import IDProcessor
from fmlaas import get_round_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import Round
from fmlaas.model import DBObject

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

    dynamodb_ = DynamoDBInterface(get_round_table_name_from_env())
    round = DBObject.load_from_db(Round, round_id, dynamodb_)

    if not round.is_in_progress() or not round.is_device_active(device_id):
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
