from .....request_processor import AuthContextProcessor
from abc import abstractmethod

class AbstractCondition:

    @abstractmethod
    def verify(self, auth_context: AuthContextProcessor) -> bool:
        raise NotImplementedError("verify() is not implemented.")
