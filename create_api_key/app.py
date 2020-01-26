import json

from fmlaas import get_auth_key_table_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import ApiKeyBuilder
from fmlaas.request_processor import IDProcessor
from fmlaas.request_processor import KeyTypeProcessor
from fedlearn_auth import generate_key_pair
from fedlearn_auth import hash_secret

def lambda_handler(event, context):
    # **WARNING**: For now, passing User ID information inside the request.
    #   This sidesteps the problem of having to set up user pools right now, before
    #   implementation has been worked out. Once that gets decided, we need to come
    #   back here and fix the glaring security flaws associated with this strategy.
    user_id = json.loads(event.get("body"))["user_id"]


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
    #   - Verify that the desired permissions for the new key do not exceed the permissions granted to the existing key

    id, key_plaintext = generate_key_pair()
    key_hash = hash_secret(key_plaintext)
    builder = ApiKeyBuilder(id, key_hash)
    builder.set_key_type(key_type)
    builder.set_entity_id(user_id)
    api_key = builder.build()

    api_key.save_to_db(dynamodb_)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"key" : key_plaintext})
    }
