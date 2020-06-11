from ...model import Job
from ...model import Project
from ...model import DBObject
from ...aws import create_presigned_url
from ...aws import get_models_bucket_name
from ...exception import raise_default_request_forbidden_error
from ...model import ProjectPrivilegeTypesEnum
from ..utils import termination_check
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from ..utils.auth.conditions import ProjectContainsJob
from ..abstract_controller import AbstractController


class GetJobAggregateModelController(AbstractController):

    def __init__(self, project_db, job_db, project_id, job_id, auth_context):
        """
        :param project_db: DB
        :param job_db: DB
        :param project_id: string
        :param job_id: string
        :param auth_context: AuthContextProcessor
        """
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
        EXPIRATION_SEC = 60 * 5

        is_job_complete = self.job.is_complete()
        if is_job_complete:
            object_name = self.job.get_aggregate_model().get_name().get_name()
            presigned_url = create_presigned_url(
                get_models_bucket_name(),
                object_name,
                expiration=EXPIRATION_SEC)
        else:
            presigned_url = None

        termination_check(self.job, self.job_db, self.project_db)

        return is_job_complete, presigned_url
