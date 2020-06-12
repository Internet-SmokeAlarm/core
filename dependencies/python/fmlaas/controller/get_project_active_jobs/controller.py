from ...database import DB
from ...model import Project
from ...model import DBObject
from ...model import ProjectPrivilegeTypesEnum
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from ..utils.auth.conditions import IsDevice
from ..utils.auth.conditions import ProjectContainsDevice
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController


class GetProjectActiveJobsController(AbstractController):

    def __init__(self, project_db: DB, project_id: str, auth_context: AuthContextProcessor):
        super(GetProjectActiveJobsController, self).__init__(auth_context)

        self.project_db = project_db
        self.project_id = project_id

    def load_data(self):
        self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ],
            [
                IsDevice(),
                ProjectContainsDevice(self.project)
            ]
        ]

    def execute_controller(self):
        return self.project.get_active_jobs()
