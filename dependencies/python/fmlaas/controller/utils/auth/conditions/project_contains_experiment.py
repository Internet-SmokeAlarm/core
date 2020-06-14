from .....request_processor import AuthContextProcessor
from .....model import Project
from .abstract_condition import AbstractCondition

class ProjectContainsExperiment(AbstractCondition):

    def __init__(self, project: Project, experiment_id: str):
        self.project = project
        self.experiment_id = experiment_id

    def verify(self, auth_context: AuthContextProcessor) -> bool:
        return self.project.contains_experiment(self.experiment_id)

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and (self.project == other.project) and (self.experiment_id == other.experiment_id)
