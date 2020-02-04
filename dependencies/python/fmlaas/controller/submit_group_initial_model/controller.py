from ...aws import create_presigned_post
from ...aws import get_models_bucket_name
from ... import HierarchicalModelNameStructure
from ...model import FLGroup
from ...model import DBObject
from ...model import GroupPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ...exception import raise_default_request_forbidden_error

def submit_group_initial_model_controller(group_db, group_id, auth_json):
    """
    :param group_db: DB
    :param group_id: string
    :param auth_json: dict
    """
    auth_context_processor = AuthContextProcessor(auth_json)
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    group = DBObject.load_from_db(FLGroup, group_id, group_db)
    if not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_WRITE):
        raise_default_request_forbidden_error()

    EXPIRATION_SEC = 60 * 10
    FIELDS = {}
    CONDITIONS = []

    model_name = HierarchicalModelNameStructure()
    model_name.generate_name(group_id=group_id)

    presigned_url = create_presigned_post(
        get_models_bucket_name(),
        model_name.get_name(),
        FIELDS,
        CONDITIONS,
        expiration=EXPIRATION_SEC)

    return presigned_url
