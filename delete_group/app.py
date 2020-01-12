import json

from fmlaas import get_group_table_name_from_env
from fmlaas import get_round_table_name_from_env
from fmlaas.aws import delete_s3_objects_with_prefix
from fmlaas.aws import get_models_bucket_name
from fmlaas.database import DynamoDBInterface
from fmlaas.model import DBObject
from fmlaas.model import FLGroup
from fmlaas.request_processor import IDProcessor

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

    group_db = DynamoDBInterface(get_group_table_name_from_env())
    round_db = DynamoDBInterface(get_round_table_name_from_env())

    try:
        group = DBObject.load_from_db(FLGroup, group_id, group_db)
        round_ids = group.get_rounds().keys()

        for round_id in round_ids:
            round_db.delete_object(round_id)

        delete_s3_objects_with_prefix(get_models_bucket_name(), group_id)

        success = group_db.delete_object(group_id)
    except:
        success = True

    return {
        "statusCode" : 200,
        "body" : json.dumps({"success" : success})
    }
