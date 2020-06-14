from .....request_processor import AuthContextProcessor
from .abstract_condition import AbstractCondition

class IsUser(AbstractCondition):

    def verify(self, auth_context: AuthContextProcessor) -> bool:
        return auth_context.is_type_user()

    def __eq__(self, other) -> bool:
        return type(other) == type(self)
