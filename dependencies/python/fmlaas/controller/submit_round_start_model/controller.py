from ...aws import create_presigned_post
from ... import HierarchicalModelNameStructure
from ...aws import get_models_bucket_name
from ...database import DynamoDBInterface
from ...model import Round
from ...model import FLGroup
from ...model import DBObject
from ...model import GroupPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error
from ..utils import termination_check

def submit_round_start_model_controller(group_db, round_db, round_id, auth_context_processor):
    """
    :param group_db: DB
    :param round_db: DB
    :param round_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    EXPIRATION_SEC = 60 * 10
    FIELDS = {}
    CONDITIONS = []

    try:
        round = DBObject.load_from_db(Round, round_id, round_db)
        group = DBObject.load_from_db(FLGroup, round.get_parent_group_id(), group_db)
    except:
        raise_default_request_forbidden_error()

    if not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_WRITE):
        raise_default_request_forbidden_error()

    can_submit_model_to_round = round.is_in_initialization()
    if can_submit_model_to_round:
        object_name = HierarchicalModelNameStructure()
        object_name.generate_name(is_start_model=True, round_id=round_id)

        presigned_url = create_presigned_post(
            get_models_bucket_name(),
            object_name.get_name(),
            FIELDS,
            CONDITIONS,
            expiration=EXPIRATION_SEC)
    else:
        presigned_url = None

    try:
        termination_check(round, round_db, group_db)
    except:
        can_submit_model_to_round = False

    return can_submit_model_to_round, presigned_url
