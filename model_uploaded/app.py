from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas import HierarchicalModelNameStructure

def lambda_handler(event, context):
    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())

    for record in event["Records"]:
        object = record["s3"]["object"]
        object_key = object["key"]

        object_name = HierarchicalModelNameStructure()
        object_name.load_name(object_key)

        group = FLGroup.load_from_db(object_name.get_group_id(), dynamodb_)
        group.add_model(object_name)

        group.save_to_db(dynamodb_)

    return {
        "statusCode" : 200,
        "body" : "{}"
    }
