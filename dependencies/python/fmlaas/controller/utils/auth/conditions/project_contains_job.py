from .....request_processor import AuthContextProcessor
from .....model import Project
from .....model import Job
from .abstract_condition import AbstractCondition

class ProjectContainsJob(AbstractCondition):

    def __init__(self, project: Project, job: Job):
        self.project = project
        self.job = job

    def verify(self, auth_context: AuthContextProcessor):
        return self.project.contains_job(self.job.get_id())

    def __eq__(self, other):
        return (type(self) == type(other)) and (self.project == other.project) and (self.job == other.job)
