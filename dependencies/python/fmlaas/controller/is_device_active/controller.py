from ...database import DB
from ...model import DBObject, Job, Project, ProjectPrivilegeTypesEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils import termination_check
from ..utils.auth.conditions import (HasProjectPermissions, IsDevice,
                                     IsEqualToAuthEntity, IsUser,
                                     JobContainsDevice, ProjectContainsJob)


class IsDeviceActiveController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 job_db: DB,
                 project_id: str,
                 job_id: str,
                 device_id: str,
                 auth_context: AuthContextProcessor):
        super(IsDeviceActiveController, self).__init__(auth_context)

        self._project_db = project_db
        self._job_db = job_db
        self._project_id = project_id
        self._job_id = job_id
        self._device_id = device_id

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
                JobContainsDevice(self._job),
                ProjectContainsJob(self._project, self._job),
                IsEqualToAuthEntity(self._device_id)
            ]
        ]

    def execute_controller(self) -> bool:
        termination_check(self._job, self._job_db, self._project_db)

        return self._job.is_device_active(self._device_id)
