from ...aws import create_presigned_url, get_models_bucket_name
from ...database import DB
from ...model import DBObject, Job, Project, ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils import termination_check
from ..utils.auth.conditions import (HasProjectPermissions, IsDevice, IsUser,
                                     JobContainsDevice, ProjectContainsJob)


class GetJobStartModelController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 job_db: DB,
                 job_id: str,
                 auth_context: AuthContextProcessor):
        super(GetJobStartModelController, self).__init__(auth_context)

        self._project_db = project_db
        self._job_db = job_db
        self._job_id = job_id

        self._job = DBObject.load_from_db(Job, self._job_id, self._job_db)
        self._project = DBObject.load_from_db(Project, self._job.project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsDevice(),
                JobContainsDevice(self._job)
            ],
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_ONLY),
                ProjectContainsJob(self._project, self._job)
            ]
        ]

    def execute_controller(self) -> str:
        EXPIRATION_SEC = 60 * 5

        termination_check(self._job, self._job_db, self._project_db)

        presigned_url = create_presigned_url(
            get_models_bucket_name(),
            str(self._job.start_model.name),
            expiration=EXPIRATION_SEC)

        return presigned_url
