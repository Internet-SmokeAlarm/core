from ...exception import raise_default_request_forbidden_error
from ...model import Project
from ...model import DBObject


def get_project_controller(db_, project_id, auth_context_processor):
    """
    :param db: DB
    :param project_id: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    project = DBObject.load_from_db(Project, project_id, db_)

    if not project.is_member(auth_context_processor.get_entity_id()):
        raise_default_request_forbidden_error()

    return project.to_json()