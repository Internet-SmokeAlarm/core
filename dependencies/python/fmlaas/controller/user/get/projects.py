from typing import List
from typing import Dict
from ...utils.auth.conditions import IsUser
from ...utils.auth.conditions import AbstractCondition
from ....database import DB
from ....request_processor import AuthContextProcessor
from ...utils.user import handle_load_user
from ...abstract_controller import AbstractController


class GetProjectsController(AbstractController):

    def __init__(self,
                 user_db: DB,
                 auth_context: AuthContextProcessor):
        super(GetProjectsController, self).__init__(auth_context)

        self._user_db = user_db

    def load_data(self) -> None:
        self._user = handle_load_user(self._user_db, self.auth_context.get_entity_id())

    def get_auth_conditions(self) -> List[List[AbstractCondition]]:
        return [
            [
                IsUser()
            ]
        ]

    def execute_controller(self) -> List[Dict[str, str]]:
        return self._user.projects
