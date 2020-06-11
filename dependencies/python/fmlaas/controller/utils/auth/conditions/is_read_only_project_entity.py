from .....model import Project
from .....model import Job
from .....model import ProjectPrivilegeTypesEnum
from .....request_processor import AuthContextProcessor
from .abstract_condition import AbstractCondition
from .is_user import IsUser
from .is_device import IsDevice
from .project_contains_device import ProjectContainsDevice
from .has_project_permissions import HasProjectPermissions
from .has_project_permissions import HasProjectPermissions


class IsReadOnlyProjectEntity(AbstractCondition):

    def __init__(self, project: Project):
        self.project = project

    def verify(self, auth_context: AuthContextProcessor):
        return (IsUser().verify(auth_context) and HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_ONLY).verify(auth_context)) or (IsDevice().verify(auth_context) and ProjectContainsDevice(self.project).verify(auth_context))

    def __eq__(self, other):
        return (type(self) == type(other)) and (self.project == other.project)
