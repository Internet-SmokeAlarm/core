from .....request_processor import AuthContextProcessor
from .....model import Project
from .abstract_condition import AbstractCondition

class ProjectContainsJobSequence(AbstractCondition):

    def __init__(self, project: Project, job_sequence_id: str):
        self.project = project
        self.job_sequence_id = job_sequence_id

    def verify(self, auth_context: AuthContextProcessor) -> bool:
        return self.project.contains_job_sequence(self.job_sequence_id)

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and (self.project == other.project) and (self.job_sequence_id == other.job_sequence_id)
