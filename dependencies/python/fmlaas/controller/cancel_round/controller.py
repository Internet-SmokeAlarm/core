from ... import generate_unique_id
from ...model import DBObject
from ...model import Round
from ...model import FLGroup
from ...exception import raise_default_request_forbidden_error
from ...model import GroupPrivilegeTypesEnum
from ..utils import update_round_path

def cancel_round_controller(group_db, round_db, round_id, auth_context_processor):
    """
    :param group_db: DB
    :param round_db: DB
    :param round_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    try:
        round = DBObject.load_from_db(Round, round_id, round_db)
        group = DBObject.load_from_db(FLGroup, round.get_parent_group_id(), group_db)
    except:
        raise_default_request_forbidden_error()

    if not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_WRITE):
        raise_default_request_forbidden_error()

    round.cancel()
    round.save_to_db(round_db)

    update_round_path(round, round_db, group_db)
