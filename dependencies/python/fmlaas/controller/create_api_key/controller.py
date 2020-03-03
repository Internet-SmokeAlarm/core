from ...model import ApiKeyBuilder
from ...model import ApiKeyTypeEnum
from ...exception import raise_default_request_forbidden_error
from fedlearn_auth import generate_key_pair
from fedlearn_auth import hash_secret

def create_api_key_controller(db_, auth_context_processor):
    """
    :param db_: DB
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    id, key_plaintext = generate_key_pair()
    key_hash = hash_secret(key_plaintext)
    builder = ApiKeyBuilder(id, key_hash)
    builder.set_key_type(ApiKeyTypeEnum.USER.value)
    builder.set_entity_id(auth_context_processor.get_entity_id())
    api_key = builder.build()

    api_key.save_to_db(db_)

    return key_plaintext
