from fmlaas.database import DynamoDBInterface
from fmlaas.aws.event_processor import AuthEventProcessor
from fmlaas.controller.auth import auth_controller
from fmlaas import get_auth_key_table_from_env

def lambda_handler(event, context):
    auth_key_db = DynamoDBInterface(get_auth_key_table_from_env())
    auth_event_processor = AuthEventProcessor()
    auth_event = auth_event_processor.process_event(event)

    return auth_controller(auth_event, auth_key_db)
