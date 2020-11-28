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
        self._experiment = self._project.get_experiment(self._experiment_id)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ]
        ]

    def execute_controller(self) -> Job:
        self._experiment.handle_termination_check()
        self._project.add_or_update_experiment(self._experiment)
        self._project.save_to_db(self._project_db)

        return self._experiment.get_job(self._job_id)
