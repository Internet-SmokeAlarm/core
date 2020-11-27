from dependencies.python.fmlaas.controller.create_api_key import \
    CreateApiKeyController
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import DBObject, User
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class CreateApiKeyControllerTestCase(AbstractTestCase):

    def test_pass(self):
        key_db = InMemoryDBInterface()
        user_db = InMemoryDBInterface()

        user, _ = self._create_empty_user(username="user_123442")
        user.save_to_db(user_db)

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = CreateApiKeyController(key_db,
                                            user_db,
                                            auth_context)

        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        self.assertEqual(auth_conditions, [
            [
                IsUser()
            ]
        ])

        # Controller execution
        key_plaintext = controller.execute()

        self.assertIsNotNone(key_plaintext)
        self.assertEqual(len(DBObject.load_from_db(User, "user_123442", user_db).api_keys), 1)
