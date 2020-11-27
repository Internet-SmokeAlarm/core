from ...database import DB
from ...model import DBObject, Project, ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import HasProjectPermissions, IsUser


class CancelJobController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 experiment_id: str,
                 job_id: str,
                 auth_context: AuthContextProcessor):
        super(CancelJobController, self).__init__(auth_context)

        self._project_db = project_db
        self._project_id = project_id
        self._experiment_id = experiment_id
        self._job_id = job_id

        self._project = DBObject.load_from_db(Project, project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

    def execute_controller(self) -> None:
        experiment = self._project.get_experiment(self._experiment_id)

        experiment.handle_termination_check()

        job = experiment.get_job(self._job_id)

        if job.is_complete():
            raise Exception("Cannot cancel a job that has already been completed.")

        job.cancel()
        experiment.add_or_update_job(job)

        self._project.add_or_update_experiment(experiment)
        self._project.save_to_db(self._project_db)