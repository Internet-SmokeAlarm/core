import unittest

from dependencies.python.fmlaas.controller.create_group import create_group_controller
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

class CreateGroupControllerTestCase(unittest.TestCase):

    def test_pass(self):
        db_ = InMemoryDBInterface()
        group_name = "hello_world"
        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user_123442"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        group_id = create_group_controller(db_, group_name, auth_context_processor)

        self.assertIsNotNone(group_id)

        loaded_group = DBObject.load_from_db(FLGroup, group_id, db_)

        self.assertEqual(loaded_group.get_id(), group_id)
        self.assertEqual(loaded_group.get_member_auth_level("user_123442"), GroupPrivilegeTypesEnum.OWNER)

    def test_fail(self):
        db_ = InMemoryDBInterface()
        group_name = "hello_world"
        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "device_123442"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, create_group_controller, db_, group_name, auth_context_processor)
