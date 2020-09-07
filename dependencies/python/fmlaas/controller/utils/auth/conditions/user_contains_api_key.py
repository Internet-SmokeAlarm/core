from .....model import User
from .....request_processor import AuthContextProcessor
from .abstract_condition import AbstractCondition


class UserContainsApiKey(AbstractCondition):

    def __init__(self, user: User, api_key_id: str):
        self._user = user
        self._api_key_id = api_key_id

    def verify(self, auth_context: AuthContextProcessor) -> bool:
        return self._user.contains_api_key(self._api_key_id)

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and (self._user == other._user) and (self._api_key_id == other._api_key_id)
