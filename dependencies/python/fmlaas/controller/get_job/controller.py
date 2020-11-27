from ...database import DB
from ...model import DBObject, Job, Project, ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import HasProjectPermissions, IsUser


class GetJobController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 experiment_id: str,
                 job_id: str,
                 auth_context: AuthContextProcessor):
        super(GetJobController, self).__init__(auth_context)

        self._project_db = project_db
        self._project_id = project_id
        self._experiment_id = experiment_id
        self._job_id = job_id

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ]
        ]

    def execute_controller(self) -> Job:
        experiment = self._project.get_experiment(self._experiment_id)

        experiment.handle_termination_check()

        return experiment.get_job(self._job_id)
