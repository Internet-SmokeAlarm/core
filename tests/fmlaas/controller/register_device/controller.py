import unittest

from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import ApiKey
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.register_device import register_device_controller
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

class RegisterDeviceControllerTestCase(unittest.TestCase):

    def _build_default_group(self):
        group_builder = GroupBuilder()
        group_builder.set_id("test_id")
        group_builder.set_name("test_name")

        group = group_builder.build()
        group.add_device("12344")
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)
        group.add_or_update_member("user_123456", GroupPrivilegeTypesEnum.READ_ONLY)

        return group

    def test_pass(self):
        group_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        group = self._build_default_group()
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        id, key_plaintext = register_device_controller(group_db_,
                                                       key_db_,
                                                       group.get_id(),
                                                       auth_context_processor)
        self.assertIsNotNone(id)
        self.assertIsNotNone(key_plaintext)
        self.assertEqual(id, DBObject.load_from_db(ApiKey, id, key_db_).get_id())

    def test_fail_not_authorized_user(self):
        group_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        group = self._build_default_group()
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        self.assertRaises(RequestForbiddenException, register_device_controller, group_db_, key_db_, group.get_id(), auth_context_processor)

    def test_fail_not_authorized_user_2(self):
        group_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        group = self._build_default_group()
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_1234567"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        self.assertRaises(RequestForbiddenException, register_device_controller, group_db_, key_db_, group.get_id(), auth_context_processor)

    def test_fail_not_authorized_device(self):
        group_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        group = self._build_default_group()
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "12344"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        self.assertRaises(RequestForbiddenException, register_device_controller, group_db_, key_db_, group.get_id(), auth_context_processor)
