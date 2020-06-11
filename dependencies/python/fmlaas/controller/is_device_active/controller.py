from ...model import DBObject
from ...model import Project
from ...model import Job
from ...model import ProjectPrivilegeTypesEnum
from ...exception import raise_default_request_forbidden_error
from ..utils import termination_check
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import IsDevice
from ..utils.auth.conditions import HasProjectPermissions
from ..utils.auth.conditions import ProjectContainsJob
from ..utils.auth.conditions import JobContainsDevice
from ..utils.auth.conditions import IsEqualToAuthEntity
from ..abstract_controller import AbstractController


class IsDeviceActiveController(AbstractController):

    def __init__(self, project_db, job_db, project_id, job_id, device_id, auth_context):
        """
        :param project_db: DB
        :param job_db: DB
        :param project_id: string
        :param job_id: string
        :param device_id: string
        :param auth_context: AuthContextProcessor
        """
        super(IsDeviceActiveController, self).__init__(auth_context)

        self.project_db = project_db
        self.job_db = job_db
        self.project_id = project_id
        self.job_id = job_id
        self.device_id = device_id

    def load_data(self):
        self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)
        self.job = DBObject.load_from_db(Job, self.job_id, self.job_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_ONLY),
                ProjectContainsJob(self.project, self.job)
            ],
            [
                IsDevice(),
                JobContainsDevice(self.job),
                ProjectContainsJob(self.project, self.job),
                IsEqualToAuthEntity(self.device_id)
            ]
        ]

    def execute_controller(self):
        termination_check(self.job, self.job_db, self.project_db)

        return self.job.is_device_active(self.device_id)
