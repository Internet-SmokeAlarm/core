from ...database import DB
from ...model import DBObject
from ...model import Job
from ...model import Project
from ...model import ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..utils import update_experiment
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from ..abstract_controller import AbstractController


class CancelJobController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 job_db: DB,
                 job_id: str,
                 auth_context: AuthContextProcessor):
        super(CancelJobController, self).__init__(auth_context)

        self._project_db = project_db
        self._job_db = job_db
        self._job_id = job_id

        self._job = DBObject.load_from_db(Job, self._job_id, self._job_db)
        self._project = DBObject.load_from_db(Project, self._job.project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

    def execute_controller(self) -> None:
        if self._job.is_complete():
            raise Exception("cannot cancel a job that has already been completed.")

        self._job.cancel()
        self._job.save_to_db(self._job_db)

        update_experiment(self._job, self._job_db, self._project_db)
