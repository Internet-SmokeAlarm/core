import json

from fmlaas import get_auth_key_table_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import ApiKeyBuilder
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import KeyTypeProcessor
from fedlearn_auth import generate_key_pair
from fedlearn_auth import hash_secret

def lambda_handler(event, context):
    req_json = event.get("pathParameters")

    try:
        id_processor = IDProcessor(req_json)
        group_id = id_processor.get_group_id()

        key_type_processor = KeyTypeProcessor(req_json)
        key_type = key_type_processor.get_key_type()
    except ValueError as error:
        return {
            "statusCode" : 400,
            "body" : str(error)
        }

    dynamodb_ = DynamoDBInterface(get_auth_key_table_from_env())

    # TODO : Verify that the user is allowed to create an API key
    #   - Set key User ID to corresponding User ID of parent key / JWT token

    id, key_plaintext = generate_key_pair()
    key_hash = hash_secret(key_plaintext)
    builder = ApiKeyBuilder(id, key_hash)
    builder.set_key_type(key_type)
    builder.set_entity_id("-1")
    api_key = builder.build()

    api_key.save_to_db(dynamodb_)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"key" : key_plaintext})
    }
