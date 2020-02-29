from ...aws import create_presigned_post
from ... import HierarchicalModelNameStructure
from ...aws import get_models_bucket_name
from ...database import DynamoDBInterface
from ...model import Round
from ...model import FLGroup
from ...model import DBObject
from ...exception import raise_default_request_forbidden_error

def submit_model_update_controller(group_db, round_db, group_id, round_id, auth_context_processor):
    """
    :param group_db: DB
    :param round_db: DB
    :param group_id: string
    :param round_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_user():
        raise_default_request_forbidden_error()

    EXPIRATION_SEC = 60 * 10
    FIELDS = {}
    CONDITIONS = []

    group = DBObject.load_from_db(FLGroup, group_id, group_db)
    if (not group.contains_round(round_id)) or (not group.contains_device(auth_context_processor.get_entity_id())):
        raise_default_request_forbidden_error()

    round = DBObject.load_from_db(Round, round_id, round_db)

    can_submit_model_to_round = round.is_in_progress() and round.is_device_active(auth_context_processor.get_entity_id())
    if can_submit_model_to_round:
        object_name = HierarchicalModelNameStructure()
        object_name.generate_name(group_id, round_id, auth_context_processor.get_entity_id())

        presigned_url = create_presigned_post(
            get_models_bucket_name(),
            object_name.get_name(),
            FIELDS,
            CONDITIONS,
            expiration=EXPIRATION_SEC)
    else:
        presigned_url = None

    return can_submit_model_to_round, presigned_url
