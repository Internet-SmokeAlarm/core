from ...model import DBObject
from ...model import Project
from ...model import Job
from ...model import ProjectPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error
from ..utils import termination_check

def is_device_active_controller(project_db, job_db, project_id, job_id, device_id, auth_context_processor):
    """
    :param project_db: DB
    :param job_db: DB
    :param project_id: string
    :param job_id: string
    :param device_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    project = DBObject.load_from_db(Project, project_id, project_db)
    if not project.contains_job(job_id):
        raise_default_request_forbidden_error()

    device_to_check = device_id
    if auth_context_processor.is_type_device():
        if (not project.contains_device(auth_context_processor.get_entity_id())) or (device_id != auth_context_processor.get_entity_id()):
            raise_default_request_forbidden_error()

        device_to_check = auth_context_processor.get_entity_id()
    elif not project.does_member_have_auth(auth_context_processor.get_entity_id(), ProjectPrivilegeTypesEnum.READ_ONLY):
        raise_default_request_forbidden_error()

    job = DBObject.load_from_db(Job, job_id, job_db)

    try:
        termination_check(job, job_db, project_db)
    except:
        pass

    return job.is_device_active(device_to_check)
