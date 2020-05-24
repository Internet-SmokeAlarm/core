from fmlaas import get_group_table_name_from_env
from fmlaas import get_job_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.aws.event_processor import ModelUploadEventProcessor
from fmlaas.controller.model_uploaded import models_uploaded_controller

def lambda_handler(event, context):
    group_db = DynamoDBInterface(get_group_table_name_from_env())
    job_db = DynamoDBInterface(get_job_table_name_from_env())

    models_uploaded = ModelUploadEventProcessor().process_event(event)

    models_uploaded_controller(group_db, job_db, models_uploaded)

    return {
        "statusCode" : 200,
        "body" : "{}"
    }
