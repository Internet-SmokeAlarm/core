from ... import generate_unique_id
from ...model import DBObject
from ...model import Job
from ...model import Project
from ...exception import raise_default_request_forbidden_error
from ...model import ProjectPrivilegeTypesEnum
from ..utils import update_job_sequence


def cancel_job_controller(project_db, job_db, job_id, auth_context_processor):
    """
    :param project_db: DB
    :param job_db: DB
    :param job_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    try:
        job = DBObject.load_from_db(Job, job_id, job_db)
        project = DBObject.load_from_db(
            Project, job.get_project_id(), project_db)
    except BaseException:
        raise_default_request_forbidden_error()

    if not project.does_member_have_auth(
            auth_context_processor.get_entity_id(), ProjectPrivilegeTypesEnum.READ_WRITE):
        raise_default_request_forbidden_error()

    if job.is_complete():
        raise Exception("cannot cancel a job that has already been completed.")

    job.cancel()
    job.save_to_db(job_db)

    update_job_sequence(job, job_db, project_db)
