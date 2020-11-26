from ...database import DB
from ...model import DBObject, Project, ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import HasProjectPermissions, IsUser


class DeleteProjectController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 job_db: DB,
                 project_id: str,
                 auth_context: AuthContextProcessor):
        super(DeleteProjectController, self).__init__(auth_context)

        self._project_db = project_db
        self._job_db = job_db
        self._project_id = project_id

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.ADMIN)
            ]
        ]

    def execute_controller(self):
        for job_id in self._project.get_all_job_ids():
            self._job_db.delete_object(job_id)

        self._project_db.delete_object(self._project_id)
