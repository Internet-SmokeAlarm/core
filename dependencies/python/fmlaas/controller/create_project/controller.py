from ... import generate_unique_id
from ...model import ProjectBuilder
from ...exception import raise_default_request_forbidden_error
from ...model import ProjectPrivilegeTypesEnum
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import IsUser

class CreateProjectController(AbstractController):

    def __init__(self, project_db, project_name, auth_context):
        """
        :param project_db: DB
        :param project_name: string
        :param auth_context: AuthContextProcessor
        """
        super(CreateProjectController, self).__init__(auth_context)

        self.project_db = project_db
        self.project_name = project_name

    def get_auth_conditions(self):
        return [
            IsUser()
        ]

    def execute_controller(self):
        project_id = generate_unique_id()

        builder = ProjectBuilder()
        builder.set_id(project_id)
        builder.set_name(self.project_name)
        project = builder.build()
        project.add_or_update_member(
            self.auth_context.get_entity_id(),
            ProjectPrivilegeTypesEnum.OWNER)

        project.save_to_db(self.project_db)

        return project_id
