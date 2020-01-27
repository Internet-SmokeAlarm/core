from ... import generate_unique_id
from ...model import GroupBuilder
from ...request_processor import AuthContextProcessor
from ...exception import RequestForbiddenException

def create_group_controller(db_, group_name, auth_json):
    """
    :param db_: DB
    :param group_name: string
    :param auth_json: dict
    """
    auth_context_processor = AuthContextProcessor(auth_json)
    if auth_context_processor.is_type_device():
        raise RequestForbiddenException("You are not authorized to access this resource")

    group_id = generate_unique_id()

    builder = GroupBuilder()
    builder.set_id(group_id)
    builder.set_name(group_name)
    group = builder.build()

    group.save_to_db(db_)

    return group_id
