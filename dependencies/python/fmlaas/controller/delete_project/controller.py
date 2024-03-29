from ...database import DB
from ...model import Project
from ...model import DBObject
from ...model import ProjectPrivilegeTypesEnum
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController


class DeleteProjectController(AbstractController):

    def __init__(self, project_db: DB, job_db: DB, project_id: str, auth_context: AuthContextProcessor):
        super(DeleteProjectController, self).__init__(auth_context)

        self.project_db = project_db
        self.job_db = job_db
        self.project_id = project_id

    def load_data(self):
        self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.ADMIN)
            ]
        ]

    def execute_controller(self):
        for job_id in self.project.get_all_job_ids():
            self.job_db.delete_object(job_id)

        self.project_db.delete_object(self.project_id)
