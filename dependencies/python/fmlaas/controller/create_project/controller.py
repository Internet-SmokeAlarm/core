from ...database import DB
from ... import generate_unique_id
from ...model import ProjectBuilder
from ...model import ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import IsUser
from ..utils.user import handle_load_user


class CreateProjectController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 user_db: DB,
                 project_name: str,
                 project_description: str,
                 auth_context: AuthContextProcessor):
        super(CreateProjectController, self).__init__(auth_context)

        self._project_db = project_db
        self._user_db = user_db
        self._project_name = project_name
        self._project_description = project_description

    def load_data(self):
        self._user = handle_load_user(self._user_db, self.auth_context.get_entity_id())

    def get_auth_conditions(self):
        return [
            [
                IsUser()
            ]
        ]

    def execute_controller(self):
        # Create a new project, save it to the project DB
        project_id = generate_unique_id()

        builder = ProjectBuilder()
        builder.set_id(project_id)
        builder.set_name(self._project_name)
        builder.set_description(self._project_description)
        project = builder.build()
        project.add_or_update_member(
            self.auth_context.get_entity_id(),
            ProjectPrivilegeTypesEnum.OWNER)

        project.save_to_db(self._project_db)

        # Associate the new project with the user, save to DB
        self._user.add_project(project_id, self._project_name)
        self._user.save_to_db(self._user_db)

        return project
