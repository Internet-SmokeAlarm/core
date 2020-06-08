import unittest

from dependencies.python.fmlaas.controller.create_api_key import CreateApiKeyController
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ApiKey
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser


class CreateApiKeyControllerTestCase(unittest.TestCase):

    def test_execute_pass(self):
        key_db = InMemoryDBInterface()
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        key_plaintext = CreateApiKeyController(key_db, auth_context).execute()

        self.assertIsNotNone(key_plaintext)

    def test_get_auth_conditions_pass(self):
        key_db = InMemoryDBInterface()
        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        auth_conditions = CreateApiKeyController(key_db, auth_context).get_auth_conditions()

        self.assertEqual(len(auth_conditions), 1)
        self.assertEqual(auth_conditions[0], IsUser())
