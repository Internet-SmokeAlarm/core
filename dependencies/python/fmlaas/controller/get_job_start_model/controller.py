from ...model import DBObject
from ...model import Project
from ...model import Job
from ...model import ProjectPrivilegeTypesEnum
from ...aws import create_presigned_url
from ...aws import get_models_bucket_name
from ...exception import raise_default_request_forbidden_error
from ..utils import termination_check


def get_job_start_model_controller(
        project_db, job_db, project_id, job_id, auth_context_processor):
    """
    :param project_db: DB
    :param job_db: DB
    :param project_id: string
    :param job_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    EXPIRATION_SEC = 60 * 5

    project = DBObject.load_from_db(Project, project_id, project_db)
    if not project.contains_job(job_id):
        raise_default_request_forbidden_error()

    job = DBObject.load_from_db(Job, job_id, job_db)

    if auth_context_processor.is_type_device():
        if not job.contains_device(auth_context_processor.get_entity_id()):
            raise_default_request_forbidden_error()
    elif not project.does_member_have_auth(auth_context_processor.get_entity_id(), ProjectPrivilegeTypesEnum.READ_ONLY):
        raise_default_request_forbidden_error()

    presigned_url = create_presigned_url(
        get_models_bucket_name(),
        job.get_start_model().get_name().get_name(),
        expiration=EXPIRATION_SEC)

    try:
        termination_check(job, job_db, project_db)
    except BaseException:
        pass

    return presigned_url
