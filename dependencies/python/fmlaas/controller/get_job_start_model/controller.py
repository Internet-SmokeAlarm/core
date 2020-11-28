from ...aws import create_presigned_url, get_models_bucket_name
from ...database import DB
from ...model import DBObject, Project, ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import (HasProjectPermissions, IsDevice, IsUser,
                                     JobContainsDevice)


class GetJobStartModelController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 experiment_id: str,
                 job_id: str,
                 auth_context: AuthContextProcessor):
        super(GetJobStartModelController, self).__init__(auth_context)

        self._project_db = project_db
        self._project_id = project_id
        self._experiment_id = experiment_id
        self._job_id = job_id

        self._project = DBObject.load_from_db(Project, project_id, self._project_db)
        self._experiment = self._project.get_experiment(self._experiment_id)
        self._job = self._experiment.get_job(self._job_id)

    def get_auth_conditions(self):
        return [
            [
                IsDevice(),
                JobContainsDevice(self._job)
            ],
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ]
        ]

    def execute_controller(self) -> str:
        EXPIRATION_SEC = 60 * 5
                
        self._experiment.handle_termination_check()
        self._project.add_or_update_experiment(self._experiment)
        self._project.save_to_db(self._project_db)

        presigned_url = create_presigned_url(
            get_models_bucket_name(),
            str(self._job.start_model.name),
            expiration=EXPIRATION_SEC)

        return presigned_url
