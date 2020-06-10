from ...model import Project
from ...model import ApiKeyBuilder
from ...model import ApiKeyTypeEnum
from ...model import DBObject
from ...model import ProjectPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error
from fedlearn_auth import generate_key_pair
from fedlearn_auth import hash_secret


def register_device_controller(
        project_db, key_db, project_id, auth_context):
    """
    :param project_db: DB
    :param key_db: DB
    :param project_id: string
    :param auth_context: AuthContextProcessor
    """
    if auth_context.is_type_device():
        raise_default_request_forbidden_error()

    project = DBObject.load_from_db(Project, project_id, project_db)
    if not project.does_member_have_auth(
            auth_context.get_entity_id(), ProjectPrivilegeTypesEnum.READ_WRITE):
        raise_default_request_forbidden_error()

    id, key_plaintext = generate_key_pair()
    key_hash = hash_secret(key_plaintext)
    builder = ApiKeyBuilder(id, key_hash)
    builder.set_key_type(ApiKeyTypeEnum.DEVICE.value)
    builder.set_entity_id(auth_context.get_entity_id())
    api_key = builder.build()
    api_key.save_to_db(key_db)

    project.add_device(api_key.get_id())
    project.save_to_db(project_db)

    return id, key_plaintext
