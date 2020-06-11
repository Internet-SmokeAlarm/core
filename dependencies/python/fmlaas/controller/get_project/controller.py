from ...model import Project
from ...model import DBObject
from ...model import ProjectPrivilegeTypesEnum
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from ..abstract_controller import AbstractController


class GetProjectController(AbstractController):

    def __init__(self, project_db, project_id, auth_context):
        """
        :param project_db: DB
        :param project_id: string
        :param auth_context: AuthContextProcessor
        """
        super(GetProjectController, self).__init__(auth_context)

        self.project_db = project_db
        self.project_id = project_id

    def load_data(self):
        self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ]
        ]

    def execute_controller(self):
        return self.project.to_json()
