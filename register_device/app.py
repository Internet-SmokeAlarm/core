import json

from fmlaas import get_group_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import FLGroup
from fmlaas.model import DBObject
from fmlaas.request_processor import IDProcessor
from fmlaas import get_auth_key_table_from_env
from fmlaas.model import ApiKeyBuilder
from fmlaas.model import ApiKeyTypeEnum
from fedlearn_auth import generate_key_pair
from fedlearn_auth import hash_secret

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

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    group = DBObject.load_from_db(FLGroup, group_id, dynamodb_)

    key_db_ = DynamoDBInterface(get_auth_key_table_from_env())

    # TODO : Add user ID from context of API key

    id, key_plaintext = generate_key_pair()
    key_hash = hash_secret(key_plaintext)
    builder = ApiKeyBuilder(id, key_hash)
    builder.set_key_type(ApiKeyTypeEnum.DEVICE.value)
    builder.set_entity_id(id)
    api_key = builder.build()
    api_key.save_to_db(key_db_)

    group.add_device(api_key.get_id())
    group.save_to_db(dynamodb_)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"device_id" : id, "device_api_key" : key_plaintext})
    }
