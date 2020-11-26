from .....model import Job, Project
from .....request_processor import AuthContextProcessor
from .abstract_condition import AbstractCondition


class ProjectContainsJob(AbstractCondition):

    def __init__(self, project: Project, job: Job):
        self._project = project
        self._job = job

    def verify(self, auth_context: AuthContextProcessor) -> bool:
        return self._project.contains_job(self._job.id)

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and \
            (self._project == other._project) and \
            (self._job == other._job)
