from ...model import DBObject
from ...model import FLGroup
from ...model import Round
from ...model import GroupPrivilegeTypesEnum
from ...aws import create_presigned_url
from ...aws import get_models_bucket_name
from ...exception import raise_default_request_forbidden_error
from ..utils import termination_check

def get_round_start_model_controller(group_db, round_db, group_id, round_id, auth_context_processor):
    """
    :param group_db: DB
    :param round_db: DB
    :param group_id: string
    :param round_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    EXPIRATION_SEC = 60 * 5

    group = DBObject.load_from_db(FLGroup, group_id, group_db)
    if not group.contains_round(round_id):
        raise_default_request_forbidden_error()

    round = DBObject.load_from_db(Round, round_id, round_db)

    if auth_context_processor.is_type_device():
        if not round.contains_device(auth_context_processor.get_entity_id()):
            raise_default_request_forbidden_error()
    elif not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_ONLY):
        raise_default_request_forbidden_error()

    presigned_url = create_presigned_url(
        get_models_bucket_name(),
        round.get_start_model().get_name().get_name(),
        expiration=EXPIRATION_SEC)

    try:
        termination_check(round, round_db, group_db)
    except:
        pass

    return presigned_url
