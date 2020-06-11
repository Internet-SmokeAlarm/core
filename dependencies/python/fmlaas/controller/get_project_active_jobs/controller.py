from ...model import Project
from ...model import DBObject
from ...model import ProjectPrivilegeTypesEnum
from ..utils.auth.conditions import IsReadOnlyProjectEntity
from ..abstract_controller import AbstractController


class GetProjectActiveJobsController(AbstractController):

    def __init__(self, project_db, project_id, auth_context):
        """
        :param project_db: DB
        :param project_id: string
        :param auth_context: AuthContextProcessor
        """
        super(GetProjectActiveJobsController, self).__init__(auth_context)

        self.project_db = project_db
        self.project_id = project_id

    def load_data(self):
        self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)

    def get_auth_conditions(self):
        return [
            [
                IsReadOnlyProjectEntity(self.project),
            ]
        ]

    def execute_controller(self):
        return self.project.get_active_jobs()
