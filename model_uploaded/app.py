import boto3
import json

from fmlaas import get_group_table_name_from_env
from fmlaas.utils import get_aggregation_lambda_func_name
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas.model import Model
from fmlaas.aws.event_processor import ModelUploadEventProcessor
from fmlaas import HierarchicalModelNameStructure

def generate_payload(group_id, round_id):
    return {
        "group_id" : group_id,
        "round_id" : round_id
    }

def trigger_aggregation_lambda_function(group_id, round_id):
    payload = json.dumps(generate_payload(group_id, round_id))

    client = boto3.client('lambda')
    client.invoke(
        FunctionName=get_aggregation_lambda_func_name(),
        InvocationType="Event",
        Payload=payload)

def lambda_handler(event, context):
    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())

    models_uploaded = ModelUploadEventProcessor().process_event(event)

    for model in models_uploaded:
        model_name = model.get_name()

        group = FLGroup.load_from_db(model_name.get_group_id(), dynamodb_)
        group.add_model(model)
        group.save_to_db(dynamodb_)

        if model_name.is_device_model_update() and group.is_round_complete(model_name.get_round_id()):
            trigger_aggregation_lambda_function(model_name.get_group_id(), model_name.get_round_id())

    return {
        "statusCode" : 200,
        "body" : "{}"
    }
