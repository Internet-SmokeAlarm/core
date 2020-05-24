from ...model import Job
from ...model import FLGroup
from ...model import DBObject
from ...aws import create_presigned_url
from ...aws import get_models_bucket_name
from ...exception import raise_default_request_forbidden_error
from ...model import GroupPrivilegeTypesEnum
from ..utils import termination_check

def get_job_aggregate_model_controller(group_db, job_db, group_id, job_id, auth_context_processor):
    """
    :param group_db: DB
    :param job_db: DB
    :param group_id: string
    :param job_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    EXPIRATION_SEC = 60 * 5

    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    group = DBObject.load_from_db(FLGroup, group_id, group_db)
    if (not group.contains_job(job_id)) or (not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_ONLY)):
        raise_default_request_forbidden_error()

    job = DBObject.load_from_db(Job, job_id, job_db)
    is_job_complete = job.is_complete()
    if is_job_complete:
        object_name = job.get_aggregate_model().get_name().get_name()
        presigned_url = create_presigned_url(get_models_bucket_name(), object_name, expiration=EXPIRATION_SEC)
    else:
        presigned_url = None

    try:
        termination_check(job, job_db, group_db)
    except:
        is_job_complete = True

    return is_job_complete, presigned_url
