from .....request_processor import AuthContextProcessor
from .abstract_condition import AbstractCondition

class IsDevice(AbstractCondition):

    def verify(self, auth_context: AuthContextProcessor):
        return auth_context.is_type_device()

    def __eq__(self, other):
        return type(other) == type(self)
