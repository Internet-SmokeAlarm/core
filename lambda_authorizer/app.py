from fmlaas.database import DynamoDBInterface
from fmlaas.aws.event_processor import AuthEventProcessor
from fmlaas.controller.auth import auth_controller
from fmlaas import get_auth_key_table_from_env

def lambda_handler(event, context):
    auth_key_db = DynamoDBInterface(get_auth_key_table_from_env())
    auth_event_processor = AuthEventProcessor(event)

    return auth_controller(auth_event_processor, auth_key_db)
