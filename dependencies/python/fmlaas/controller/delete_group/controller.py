from ...model import FLGroup
from ...model import DBObject
from ...model import GroupPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error

def delete_group_controller(group_db, round_db, group_id, auth_context_processor):
    """
    :param group_db: DB
    :param round_db: DB
    :param group_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    try:
        group = DBObject.load_from_db(FLGroup, group_id, group_db)
    except:
        raise_default_request_forbidden_error()

    if not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.ADMIN):
        raise_default_request_forbidden_error()

    round_ids = group.get_round_info().keys()
    for round_id in round_ids:
        round_db.delete_object(round_id)

    group_db.delete_object(group_id)
