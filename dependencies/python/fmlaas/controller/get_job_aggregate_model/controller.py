from ...database import DB
from ...model import Job
from ...model import Project
from ...model import DBObject
from ...aws import create_presigned_url
from ...aws import get_models_bucket_name
from ...model import ProjectPrivilegeTypesEnum
from ..utils import termination_check
from ...request_processor import AuthContextProcessor
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from ..utils.auth.conditions import ProjectContainsJob
from ..abstract_controller import AbstractController


class GetJobAggregateModelController(AbstractController):

    def __init__(self, project_db: DB, job_db: DB, project_id: str, job_id: str, auth_context: AuthContextProcessor):
        super(GetJobAggregateModelController, self).__init__(auth_context)

        self.project_db = project_db
        self.job_db = job_db
        self.project_id = project_id
        self.job_id = job_id

    def load_data(self):
        self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)
        self.job = DBObject.load_from_db(Job, self.job_id, self.job_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_ONLY),
                ProjectContainsJob(self.project, self.job)
            ]
        ]

    def execute_controller(self):
        EXPIRATION_SEC = 60

        termination_check(self.job, self.job_db, self.project_db)

        if not self.job.is_complete():
            raise ValueError("Cannot get aggregate model for incomplete job")

        s3_object_pointer = self.job.get_aggregate_model().get_name()
        presigned_url = create_presigned_url(
            get_models_bucket_name(),
            str(s3_object_pointer),
            expiration=EXPIRATION_SEC)

        return presigned_url
