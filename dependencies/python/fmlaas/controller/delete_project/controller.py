from ...model import Project
from ...model import DBObject
from ...model import ProjectPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error

def delete_project_controller(project_db, job_db, project_id, auth_context_processor):
    """
    :param project_db: DB
    :param job_db: DB
    :param project_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    try:
        project = DBObject.load_from_db(Project, project_id, project_db)
    except:
        raise_default_request_forbidden_error()

    if not project.does_member_have_auth(auth_context_processor.get_entity_id(), ProjectPrivilegeTypesEnum.ADMIN):
        raise_default_request_forbidden_error()

    job_ids = project.get_job_info().keys()
    for job_id in job_ids:
        job_db.delete_object(job_id)

    project_db.delete_object(project_id)
