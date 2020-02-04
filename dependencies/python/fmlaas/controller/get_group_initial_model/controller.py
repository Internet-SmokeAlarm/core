from ...model import FLGroup
from ...model import DBObject
from ...aws import create_presigned_url
from ...aws import get_models_bucket_name
from ...exception import raise_default_request_forbidden_error
from ...request_processor import AuthContextProcessor
from ...model import GroupPrivilegeTypesEnum

def get_group_initial_model_controller(db, group_id, auth_json):
    """
    :param db: DB
    :param group_id: string
    :param auth_json: dict
    """
    EXPIRATION_SEC = 60 * 5

    # Want to optimize load time...do 2 separate checks sequentially, preventing
    #   need to run DB query in some instances.
    auth_context_processor = AuthContextProcessor(auth_json)
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    group = DBObject.load_from_db(FLGroup, group_id, db)
    if not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_ONLY):
        raise_default_request_forbidden_error()

    is_initial_model_set = group.is_initial_model_set()
    if is_initial_model_set:
        presigned_url = create_presigned_url(
            get_models_bucket_name(),
            group.get_initial_model().get_name().get_name(),
            expiration=EXPIRATION_SEC)
    else:
        presigned_url = None

    return is_initial_model_set, presigned_url
