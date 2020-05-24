from ...aws import create_presigned_post
from ... import HierarchicalModelNameStructure
from ...aws import get_models_bucket_name
from ...database import DynamoDBInterface
from ...model import Job
from ...model import Project
from ...model import DBObject
from ...exception import raise_default_request_forbidden_error
from ..utils import termination_check

def submit_model_update_controller(project_db, job_db, project_id, job_id, auth_context_processor):
    """
    :param project_db: DB
    :param job_db: DB
    :param project_id: string
    :param job_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_user():
        raise_default_request_forbidden_error()

    EXPIRATION_SEC = 60 * 10
    FIELDS = {}
    CONDITIONS = []

    project = DBObject.load_from_db(Project, project_id, project_db)
    if (not project.contains_job(job_id)) or (not project.contains_device(auth_context_processor.get_entity_id())):
        raise_default_request_forbidden_error()

    job = DBObject.load_from_db(Job, job_id, job_db)

    can_submit_model_to_job = job.is_in_progress() and job.is_device_active(auth_context_processor.get_entity_id())
    if can_submit_model_to_job:
        object_name = HierarchicalModelNameStructure()
        object_name.generate_name(job_id=job_id, device_id=auth_context_processor.get_entity_id())

        presigned_url = create_presigned_post(
            get_models_bucket_name(),
            object_name.get_name(),
            FIELDS,
            CONDITIONS,
            expiration=EXPIRATION_SEC)
    else:
        presigned_url = None

    try:
        termination_check(job, job_db, project_db)
    except:
        can_submit_model_to_job = False

    return can_submit_model_to_job, presigned_url
