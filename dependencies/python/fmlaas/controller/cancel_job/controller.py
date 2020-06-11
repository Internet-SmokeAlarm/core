from ... import generate_unique_id
from ...model import DBObject
from ...model import Job
from ...model import Project
from ...exception import raise_default_request_forbidden_error
from ...model import ProjectPrivilegeTypesEnum
from ..utils import update_job_sequence
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from ..abstract_controller import AbstractController


class CancelJobController(AbstractController):

    def __init__(self, project_db, job_db, job_id, auth_context):
        """
        :param project_db: DB
        :param job_db: DB
        :param job_id: string
        :param auth_context: AuthContextProcessor
        """
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
