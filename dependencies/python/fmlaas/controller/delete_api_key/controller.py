from ..abstract_controller import AbstractController
from ...database import DB
from ...request_processor import AuthContextProcessor
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import UserContainsApiKey
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

    def load_data(self):
        # TODO
        # NOTE: The following *MIGHT* be a security vulnerability. If someone passes in a
        # non-user auth context, then the following line will create a user with the entity ID.
        # Need to find a way to fix this...Maybe only provision users when they sign-up in the
        # Cognito user pool?
        self._user = handle_load_user(self._user_db, self.auth_context.get_entity_id())

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                UserContainsApiKey(self._user, self._api_key_id)
            ]
        ]

    def execute_controller(self):
        self._api_key_db.delete_object(self._api_key_id)
        self._user.remove_api_key(self._api_key_id)
        self._user.save_to_db(self._user_db)
