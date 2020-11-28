from typing import List

from ...database import DB
from ...model import DBObject, Project, ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import (HasProjectPermissions, IsDevice, IsUser,
                                     ProjectContainsDevice)


class GetProjectActiveJobsController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 auth_context: AuthContextProcessor):
        super(GetProjectActiveJobsController, self).__init__(auth_context)

        self._project_db = project_db
        self._project_id = project_id

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ],
            [
                IsDevice(),
                ProjectContainsDevice(self._project)
            ]
        ]

    def execute_controller(self) -> List[str]:
        active_jobs = list()
        if self.auth_context.is_type_device():
            active_jobs = self._project.get_active_jobs_for_device(self.auth_context.get_entity_id())
        else:
            active_jobs = self._project.get_active_jobs()

        return active_jobs
