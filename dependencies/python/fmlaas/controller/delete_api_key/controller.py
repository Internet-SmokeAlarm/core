from ...database import DB
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import IsUser, UserContainsApiKey
from ..utils.user import handle_load_user


class DeleteApiKeyController(AbstractController):

    def __init__(self,
                 api_key_db: DB,
                 user_db: DB,
                 api_key_id: str,
                 auth_context: AuthContextProcessor):
        super(DeleteApiKeyController, self).__init__(auth_context)

        self._api_key_db = api_key_db
        self._user_db = user_db
        self._api_key_id = api_key_id

        self._user = handle_load_user(self._user_db, self.auth_context.get_entity_id())

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                UserContainsApiKey(self._user, self._api_key_id)
            ]
        ]

    def execute_controller(self) -> None:
        self._api_key_db.delete_object(self._api_key_id)
        self._user.remove_api_key(self._api_key_id)
        self._user.save_to_db(self._user_db)
