from ... import generate_unique_id
from ...model import ProjectBuilder
from ...exception import raise_default_request_forbidden_error
from ...model import ProjectPrivilegeTypesEnum


def create_project_controller(db_, project_name, auth_context_processor):
    """
    :param db_: DB
    :param project_name: string
    :param auth_context_processor: AuthContextProcessor
    """
    if auth_context_processor.is_type_device():
        raise_default_request_forbidden_error()

    project_id = generate_unique_id()

    builder = ProjectBuilder()
    builder.set_id(project_id)
    builder.set_name(project_name)
    project = builder.build()
    project.add_or_update_member(
        auth_context_processor.get_entity_id(),
        ProjectPrivilegeTypesEnum.OWNER)

    project.save_to_db(db_)

    return project_id
