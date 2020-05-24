from ...model import DBObject
from ...model import FLGroup
from ...model import Job
from ...model import GroupPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error
from ..utils import termination_check

def is_device_active_controller(group_db, job_db, group_id, job_id, device_id, auth_context_processor):
    """
    :param group_db: DB
    :param job_db: DB
    :param group_id: string
    :param job_id: string
    :param device_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    group = DBObject.load_from_db(FLGroup, group_id, group_db)
    if not group.contains_job(job_id):
        raise_default_request_forbidden_error()

    device_to_check = device_id
    if auth_context_processor.is_type_device():
        if (not group.contains_device(auth_context_processor.get_entity_id())) or (device_id != auth_context_processor.get_entity_id()):
            raise_default_request_forbidden_error()

        device_to_check = auth_context_processor.get_entity_id()
    elif not group.does_member_have_auth(auth_context_processor.get_entity_id(), GroupPrivilegeTypesEnum.READ_ONLY):
        raise_default_request_forbidden_error()

    job = DBObject.load_from_db(Job, job_id, job_db)

    try:
        termination_check(job, job_db, group_db)
    except:
        pass

    return job.is_device_active(device_to_check)
