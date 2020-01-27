import unittest

from dependencies.python.fmlaas.controller.create_group import create_group_controller
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException

class CreateGroupControllerTestCase(unittest.TestCase):

    def test_pass(self):
        db_ = InMemoryDBInterface()
        group_name = "hello_world"
        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user_123442"
        }

        group_id = create_group_controller(db_, group_name, auth_json)

        self.assertIsNotNone(group_id)

    def test_fail(self):
        db_ = InMemoryDBInterface()
        group_name = "hello_world"
        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "device_123442"
        }

        self.assertRaises(RequestForbiddenException, create_group_controller, db_, group_name, auth_json)
