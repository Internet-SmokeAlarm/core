from ...model import Project
from ...model import DBObject
from ...exception import raise_default_request_forbidden_error


def get_project_active_jobs_controller(
        db, project_id, auth_context):
    """
    :param db: DB
    :param project_id: string
    :param auth_context: AuthContextProcessor
    """
    project = DBObject.load_from_db(Project, project_id, db)

    if (auth_context.is_type_device() and not project.contains_device(auth_context.get_entity_id())) or (
            auth_context.is_type_user() and not project.is_member(auth_context.get_entity_id())):
        raise_default_request_forbidden_error()

    return project.get_active_jobs()
