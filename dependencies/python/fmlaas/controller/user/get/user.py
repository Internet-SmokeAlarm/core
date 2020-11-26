from typing import List

from ....database import DB
from ....model import User
from ....request_processor import AuthContextProcessor
from ...abstract_controller import AbstractController
from ...utils.auth.conditions import AbstractCondition, IsUser
from ...utils.user import handle_load_user


class GetUserController(AbstractController):

    def __init__(self,
                 user_db: DB,
                 auth_context: AuthContextProcessor):
        super(GetUserController, self).__init__(auth_context)

        self._user_db = user_db

        self._user = handle_load_user(self._user_db, self.auth_context.get_entity_id())

    def get_auth_conditions(self) -> List[List[AbstractCondition]]:
        return [
            [
                IsUser()
            ]
        ]

    def execute_controller(self) -> User:
        return self._user
