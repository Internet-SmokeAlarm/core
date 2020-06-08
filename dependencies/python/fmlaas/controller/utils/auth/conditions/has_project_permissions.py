from .....model import Project
from .....model import ProjectPrivilegeTypesEnum
from .....request_processor import AuthContextProcessor
from .abstract_condition import AbstractCondition


class HasProjectPermissions(AbstractCondition):

    def __init__(self, project: Project, permission_level: ProjectPrivilegeTypesEnum):
        self.project = project
        self.permission_level = permission_level

    def verify(self, auth_context: AuthContextProcessor):
        return self.project.does_member_have_auth(auth_context.get_entity_id(), self.permission_level)
