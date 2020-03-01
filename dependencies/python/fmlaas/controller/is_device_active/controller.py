from ...model import DBObject
from ...model import FLGroup
from ...model import Round
from ...model import GroupPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error
from ..utils import termination_check

def is_device_active_controller(group_db, round_db, group_id, round_id, device_id, auth_context_processor):
    """
    :param group_db: DB
    :param round_db: DB
    :param group_id: string
    :param round_id: string
    :param device_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    group = DBObject.load_from_db(FLGroup, group_id, group_db)
    if not group.contains_round(round_id):
        raise_default_request_forbidden_error()

    round = DBObject.load_from_db(Round, round_id, round_db)

    device_to_check = device_id
    if auth_context_processor.is_type_device():
        if (not group.contains_device(auth_context_processor.get_entity_id())) or (device_id is not auth_context_processor.get_entity_id()):
            raise_default_request_forbidden_error()

        device_to_check = auth_context_processor.get_entity_id()
    elif not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_ONLY):
        raise_default_request_forbidden_error()

    try:
        termination_check(round, round_db, group_db)
    except:
        pass

    return round.is_device_active(device_to_check)
