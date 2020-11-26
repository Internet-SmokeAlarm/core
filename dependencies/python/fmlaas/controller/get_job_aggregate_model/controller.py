from ...aws import create_presigned_url, get_models_bucket_name
from ...database import DB
from ...model import DBObject, Job, Project, ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils import termination_check
from ..utils.auth.conditions import (HasProjectPermissions, IsDevice, IsUser,
                                     ProjectContainsDevice, ProjectContainsJob)


class GetJobAggregateModelController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 job_db: DB,
                 project_id: str,
                 job_id: str,
                 auth_context: AuthContextProcessor):
        super(GetJobAggregateModelController, self).__init__(auth_context)

        self._project_db = project_db
        self._job_db = job_db
        self._project_id = project_id
        self._job_id = job_id

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)
        self._job = DBObject.load_from_db(Job, self._job_id, self._job_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_ONLY),
                ProjectContainsJob(self._project, self._job)
            ],
            [
                IsDevice(),
                ProjectContainsJob(self._project, self._job),
                ProjectContainsDevice(self._project)
            ]
        ]

    def execute_controller(self) -> str:
        EXPIRATION_SEC = 60

        termination_check(self._job, self._job_db, self._project_db)

        if not self._job.is_complete():
            raise ValueError("Cannot get aggregate model for incomplete job")

        s3_object_pointer = self._job.aggregate_model.name
        presigned_url = create_presigned_url(
            get_models_bucket_name(),
            str(s3_object_pointer),
            expiration=EXPIRATION_SEC)

        return presigned_url
