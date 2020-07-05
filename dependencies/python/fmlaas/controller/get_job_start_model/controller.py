from ...database import DB
from ...model import Job
from ...model import Project
from ...model import DBObject
from ...aws import create_presigned_url
from ...aws import get_models_bucket_name
from ..utils import termination_check
from ...model import ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..utils.auth.conditions import ProjectContainsJob
from ..utils.auth.conditions import JobContainsDevice
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import IsDevice
from ..utils.auth.conditions import HasProjectPermissions
from ..abstract_controller import AbstractController


class GetJobStartModelController(AbstractController):

    def __init__(self, project_db: DB, job_db: DB, job_id: str, auth_context: AuthContextProcessor):
        super(GetJobStartModelController, self).__init__(auth_context)

        self.project_db = project_db
        self.job_db = job_db
        self.job_id = job_id

    def load_data(self):
        self.job = DBObject.load_from_db(Job, self.job_id, self.job_db)
        self.project = DBObject.load_from_db(Project, self.job.get_project_id(), self.project_db)

    def get_auth_conditions(self):
        return [
            [
                IsDevice(),
                JobContainsDevice(self.job)
            ],
            [
                IsUser(),
                HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_ONLY),
                ProjectContainsJob(self.project, self.job)
            ]
        ]

    def execute_controller(self):
        EXPIRATION_SEC = 60 * 5

        termination_check(self.job, self.job_db, self.project_db)

        presigned_url = create_presigned_url(
            get_models_bucket_name(),
            str(self.job.get_start_model().get_name()),
            expiration=EXPIRATION_SEC)

        return presigned_url
