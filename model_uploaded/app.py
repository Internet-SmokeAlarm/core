from fmlaas import get_group_table_name_from_env
from fmlaas import get_round_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.aws.event_processor import ModelUploadEventProcessor
from fmlaas.controller.models_uploaded import models_uploaded_controller

def lambda_handler(event, context):
    group_db = DynamoDBInterface(get_group_table_name_from_env())
    round_db = DynamoDBInterface(get_round_table_name_from_env())

    models_uploaded = ModelUploadEventProcessor().process_event(event)

    models_uploaded_controller(group_db, round_db, models_uploaded)

    return {
        "statusCode" : 200,
        "body" : "{}"
    }
