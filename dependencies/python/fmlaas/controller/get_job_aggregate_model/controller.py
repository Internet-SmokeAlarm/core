from ...model import Job
from ...model import Project
from ...model import DBObject
from ...aws import create_presigned_url
from ...aws import get_models_bucket_name
from ...exception import raise_default_request_forbidden_error
from ...model import ProjectPrivilegeTypesEnum
from ..utils import termination_check


def get_job_aggregate_model_controller(
        project_db, job_db, project_id, job_id, auth_context):
    """
    :param project_db: DB
    :param job_db: DB
    :param project_id: string
    :param job_id: string
    :param auth_context: AuthContextProcessor
    """
    EXPIRATION_SEC = 60 * 5

    if auth_context.is_type_device():
        raise_default_request_forbidden_error()

    project = DBObject.load_from_db(Project, project_id, project_db)
    if (not project.contains_job(job_id)) or (not project.does_member_have_auth(
            auth_context.get_entity_id(), ProjectPrivilegeTypesEnum.READ_ONLY)):
        raise_default_request_forbidden_error()

    job = DBObject.load_from_db(Job, job_id, job_db)
    is_job_complete = job.is_complete()
    if is_job_complete:
        object_name = job.get_aggregate_model().get_name().get_name()
        presigned_url = create_presigned_url(
            get_models_bucket_name(),
            object_name,
            expiration=EXPIRATION_SEC)
    else:
        presigned_url = None

    try:
        termination_check(job, job_db, project_db)
    except BaseException:
        is_job_complete = True

    return is_job_complete, presigned_url
