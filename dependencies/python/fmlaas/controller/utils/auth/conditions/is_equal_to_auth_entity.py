from .....request_processor import AuthContextProcessor
from .abstract_condition import AbstractCondition

class IsEqualToAuthEntity(AbstractCondition):

    def __init__(self, obj1):
        self.obj1 = obj1

    def verify(self, auth_context: AuthContextProcessor) -> bool:
        return self.obj1 == auth_context.get_entity_id()

    def __eq__(self, other) -> bool:
        return (type(other) == type(self)) and (self.obj1 == other.obj1)
