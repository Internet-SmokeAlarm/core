from ...model import FLGroup
from ...model import GroupPrivilegeTypesEnum
from ...model import Job
from ...model import DBObject
from ...exception import raise_default_request_forbidden_error
from ..utils import termination_check

def get_job_controller(group_db, job_db, group_id, job_id, auth_context_processor):
    """
    :param group_db: DB
    :param job_db: DB
    :param group_id: string
    :param job_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    group = DBObject.load_from_db(FLGroup, group_id, group_db)
    if (not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_ONLY)) or (not group.contains_job(job_id)):
        raise_default_request_forbidden_error()

    job = DBObject.load_from_db(Job, job_id, job_db)
    try:
        termination_check(job, job_db, group_db)
    except:
        pass

    return job
