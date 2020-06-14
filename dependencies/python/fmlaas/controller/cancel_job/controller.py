from ...database import DB
from ...model import DBObject
from ...model import Job
from ...model import Project
from ...model import ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..utils import update_job_sequence
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from ..abstract_controller import AbstractController


class CancelJobController(AbstractController):

    def __init__(self, project_db: DB, job_db: DB, job_id: str, auth_context: AuthContextProcessor):
        super(CancelJobController, self).__init__(auth_context)

        self.project_db = project_db
        self.job_db = job_db
        self.job_id = job_id

    def load_data(self):
        self.job = DBObject.load_from_db(Job, self.job_id, self.job_db)
        self.project = DBObject.load_from_db(Project, self.job.get_project_id(), self.project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

    def execute_controller(self):
        if self.job.is_complete():
            raise Exception("cannot cancel a job that has already been completed.")

        self.job.cancel()
        self.job.save_to_db(self.job_db)

        update_job_sequence(self.job, self.job_db, self.project_db)
