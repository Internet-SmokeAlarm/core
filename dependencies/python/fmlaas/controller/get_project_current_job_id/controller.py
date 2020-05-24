from ...model import Project
from ...model import DBObject
from ...exception import raise_default_request_forbidden_error


def get_project_current_job_id_controller(
        db, project_id, auth_context_processor):
    """
    :param db: DB
    :param project_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    project = DBObject.load_from_db(Project, project_id, db)

    if (auth_context_processor.is_type_device() and not project.contains_device(auth_context_processor.get_entity_id())) or (
            auth_context_processor.is_type_user() and not project.is_member(auth_context_processor.get_entity_id())):
        raise_default_request_forbidden_error()

    return project.get_current_job_ids()
