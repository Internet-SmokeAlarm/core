from ...model import FLGroup
from ...model import DBObject
from ...exception import raise_default_request_forbidden_error

def get_group_current_round_id_controller(db, group_id, auth_context_processor):
    """
    :param db: DB
    :param group_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    group = DBObject.load_from_db(FLGroup, group_id, db)

    if (auth_context_processor.is_type_device() and not group.contains_device(auth_context_processor.get_entity_id())) or (auth_context_processor.is_type_user() and not group.is_member(auth_context_processor.get_entity_id())):
        raise_default_request_forbidden_error()

    return group.get_current_round_ids()
