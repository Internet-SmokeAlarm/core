from ...exception import raise_default_request_forbidden_error
from ...model import FLGroup
from ...model import DBObject

def get_group_controller(db_, group_id, auth_context_processor):
    """
    :param db: DB
    :param group_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    group = DBObject.load_from_db(FLGroup, group_id, db_)

    if not group.is_member(auth_context_processor.get_entity_id()):
        raise_default_request_forbidden_error()

    return group.to_json()
