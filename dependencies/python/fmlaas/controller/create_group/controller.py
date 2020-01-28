from ... import generate_unique_id
from ...model import GroupBuilder
from ...request_processor import AuthContextProcessor
from ...exception import raise_default_request_forbidden_error
from ...model import GroupPrivilegeTypesEnum

def create_group_controller(db_, group_name, auth_json):
    """
    :param db_: DB
    :param group_name: string
    :param auth_json: dict
    """
    auth_context_processor = AuthContextProcessor(auth_json)
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    group_id = generate_unique_id()

    builder = GroupBuilder()
    builder.set_id(group_id)
    builder.set_name(group_name)
    group = builder.build()
    group.add_or_update_member(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.OWNER)

    group.save_to_db(db_)

    return group_id
