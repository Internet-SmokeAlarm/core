from ..abstract_testcase import AbstractTestCase
from dependencies.python.fmlaas.controller.delete_api_key import DeleteApiKeyController
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ApiKey
from dependencies.python.fmlaas.model import User
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions import UserContainsApiKey


class DeleteApiKeyControllerTestCase(AbstractTestCase):

    def test_execute_pass(self):
        key_db = InMemoryDBInterface()
        user_db = InMemoryDBInterface()

        api_key = self._build_simple_api_key()
        api_key.api_key.save_to_db(key_db)

        user = self._create_empty_user()
        user.user.add_api_key(api_key.id)
        user.user.save_to_db(user_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": user.username
        }
        auth_context = AuthContextProcessor(auth_json)

        DeleteApiKeyController(key_db,
                               user_db,
                               api_key.id,
                               auth_context).execute()

        self.assertRaises(ValueError, DBObject.load_from_db, ApiKey, api_key.id, key_db)
        self.assertEqual(DBObject.load_from_db(User, user.username, user_db).api_keys, list())

    def test_load_data_pass(self):
        key_db = InMemoryDBInterface()
        user_db = InMemoryDBInterface()

        api_key = self._build_simple_api_key()
        api_key.api_key.save_to_db(key_db)

        user = self._create_empty_user()
        user.user.add_api_key(api_key.id)
        user.user.save_to_db(user_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": user.username
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = DeleteApiKeyController(key_db,
                                            user_db,
                                            api_key.id,
                                            auth_context)
        controller.load_data()

        self.assertEqual(controller._user, user.user)

    def test_get_auth_conditions_pass(self):
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
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser(),
                UserContainsApiKey(user.user, api_key.id)
            ]
        ]

        self.assertEqual(correct_auth_conditions, auth_conditions)
