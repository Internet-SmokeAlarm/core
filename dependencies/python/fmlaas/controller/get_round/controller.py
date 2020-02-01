from ...model import FLGroup
from ...model import GroupPrivilegeTypesEnum
from ...model import Round
from ...model import DBObject
from ...request_processor import AuthContextProcessor
from ...exception import raise_default_request_forbidden_error

def get_round_controller(group_db, round_db, group_id, round_id, auth_json):
    """
    :param group_db: DB
    :param round_db: DB
    :param group_id: string
    :param round_id: string
    :param auth_json: dict
    """
    auth_context_processor = AuthContextProcessor(auth_json)
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    group = DBObject.load_from_db(FLGroup, group_id, group_db)
    if (not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_ONLY)) or (not group.contains_round(round_id)):
        raise_default_request_forbidden_error()

    return DBObject.load_from_db(Round, round_id, round_db)
