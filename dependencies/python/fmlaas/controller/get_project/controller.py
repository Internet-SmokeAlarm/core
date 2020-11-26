from ...database import DB
from ...model import DBObject, Project, ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import HasProjectPermissions, IsUser


class GetProjectController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 auth_context: AuthContextProcessor):
        super(GetProjectController, self).__init__(auth_context)

        self._project_db = project_db
        self._project_id = project_id

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ]
        ]

    def execute_controller(self) -> dict:
        return self._project.to_json()
