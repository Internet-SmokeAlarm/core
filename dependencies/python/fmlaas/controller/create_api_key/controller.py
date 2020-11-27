from ...database import DB
from ...model import ApiKeyFactory, ApiKeyTypeEnum
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import IsUser
from ..utils.user import handle_load_user


class CreateApiKeyController(AbstractController):

    def __init__(self,
                 key_db: DB,
                 user_db: DB,
                 auth_context: AuthContextProcessor):
        super(CreateApiKeyController, self).__init__(auth_context)

        self._key_db = key_db
        self._user_db = user_db

        self._user = handle_load_user(self._user_db, self._auth_context.get_entity_id())

    def get_auth_conditions(self):
        return [
            [
                IsUser()
            ]
        ]

    def execute_controller(self) -> str:
        api_key, key_plaintext = ApiKeyFactory.create_api_key(self.auth_context.get_entity_id(),
                                                              ApiKeyTypeEnum.USER)

        # Save API Key to DB
        api_key.save_to_db(self._key_db)

        # Register API Key with User
        self._user.add_api_key(id)
        self._user.save_to_db(self._user_db)

        return key_plaintext
