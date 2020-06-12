from .....model import Job
from .....request_processor import AuthContextProcessor
from .abstract_condition import AbstractCondition

class JobContainsDevice(AbstractCondition):

    def __init__(self, job: Job):
        self.job = job

    def verify(self, auth_context: AuthContextProcessor) -> bool:
        return self.job.contains_device(auth_context.get_entity_id())

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and (self.job == other.job)
