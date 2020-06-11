from .....model import Project
from .....model import Job
from .....model import ProjectPrivilegeTypesEnum
from .....request_processor import AuthContextProcessor
from .abstract_condition import AbstractCondition
from .is_user import IsUser
from .is_device import IsDevice
from .job_contains_device import JobContainsDevice
from .has_project_permissions import HasProjectPermissions
from .has_project_permissions import HasProjectPermissions


class IsReadOnlyEntity(AbstractCondition):

    def __init__(self, project: Project, job: Job):
        self.project = project
        self.job = job

    def verify(self, auth_context: AuthContextProcessor):
        return (IsUser().verify(auth_context) and HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_ONLY).verify(auth_context)) or (IsDevice().verify(auth_context) and JobContainsDevice(self.job).verify(auth_context))

    def __eq__(self, other):
        return (type(self) == type(other)) and (self.project == other.project) and (self.job == other.job)
