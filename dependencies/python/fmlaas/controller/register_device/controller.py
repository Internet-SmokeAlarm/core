from ...model import FLGroup
from ...model import ApiKeyBuilder
from ...model import ApiKeyTypeEnum
from ...model import DBObject
from ...model import GroupPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error
from fedlearn_auth import generate_key_pair
from fedlearn_auth import hash_secret

def register_device_controller(group_db, key_db, group_id, auth_context_processor):
    """
    :param group_db: DB
    :param key_db: DB
    :param group_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    group = DBObject.load_from_db(FLGroup, group_id, group_db)
    if not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_WRITE):
        raise_default_request_forbidden_error()

    id, key_plaintext = generate_key_pair()
    key_hash = hash_secret(key_plaintext)
    builder = ApiKeyBuilder(id, key_hash)
    builder.set_key_type(ApiKeyTypeEnum.DEVICE.value)
    builder.set_entity_id(auth_context_processor.get_entity_id())
    api_key = builder.build()
    api_key.save_to_db(key_db)

    group.add_device(api_key.get_id())
    group.save_to_db(group_db)

    return id, key_plaintext
