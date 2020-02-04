import unittest

from dependencies.python.fmlaas.controller.create_api_key import create_api_key_controller
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ApiKey
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum

class CreateApiKeyControllerTestCase(unittest.TestCase):

    def test_pass_1(self):
        db_ = InMemoryDBInterface()
        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user_123442"
        }

        key_plaintext = create_api_key_controller(db_, auth_json)

        self.assertIsNotNone(key_plaintext)

    def test_pass_2(self):
        db_ = InMemoryDBInterface()
        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123442"
        }

        key_plaintext = create_api_key_controller(db_, auth_json)

        self.assertIsNotNone(key_plaintext)

    def test_unauthorized(self):
        db_ = InMemoryDBInterface()
        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "user_123442"
        }

        self.assertRaises(RequestForbiddenException, create_api_key_controller, db_, auth_json)
