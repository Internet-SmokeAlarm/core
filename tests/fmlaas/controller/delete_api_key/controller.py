from dependencies.python.fmlaas.controller.delete_api_key import \
    DeleteApiKeyController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    IsUser, UserContainsApiKey)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import ApiKey, DBObject, User
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class DeleteApiKeyControllerTestCase(AbstractTestCase):

    def test_pass(self):
        key_db = InMemoryDBInterface()
        user_db = InMemoryDBInterface()

        api_key = self._build_simple_api_key()
        api_key.api_key.save_to_db(key_db)

        user = self._create_empty_user()
        user.user.add_api_key(api_key.id)
        user.user.save_to_db(user_db)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": user.username
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = DeleteApiKeyController(key_db,
                                            user_db,
                                            api_key.id,
                                            auth_context)

        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser(),
                UserContainsApiKey(user.user, api_key.id)
            ]
        ]

        self.assertEqual(correct_auth_conditions, auth_conditions)

        # Execute
        controller.execute()
        self.assertRaises(ValueError, DBObject.load_from_db, ApiKey, api_key.id, key_db)
        self.assertEqual(DBObject.load_from_db(User, user.username, user_db).api_keys, list())
