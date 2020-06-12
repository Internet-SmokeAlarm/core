from .....model import Project
from .....request_processor import AuthContextProcessor
from .abstract_condition import AbstractCondition

class ProjectContainsDevice(AbstractCondition):

    def __init__(self, project: Project):
        self.project = project

    def verify(self, auth_context: AuthContextProcessor) -> bool:
        return self.project.contains_device(auth_context.get_entity_id())

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and (self.project == other.project)
