import unittest

from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.submit_group_initial_model import submit_group_initial_model_controller

class SubmitGroupInitialModelControllerTestCase(unittest.TestCase):

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

        group = self._build_default_group()
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        presigned_url = submit_group_initial_model_controller(group_db_,
                                                              group.get_id(),
                                                              auth_json)
        self.assertIsNotNone(presigned_url)

    def test_fail_not_authorized_device(self):
        group_db_ = InMemoryDBInterface()

        group = self._build_default_group()
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "12344"
        }
        self.assertRaises(RequestForbiddenException, submit_group_initial_model_controller, group_db_, group.get_id(), auth_json)

    def test_fail_not_authorized_user(self):
        group_db_ = InMemoryDBInterface()

        group = self._build_default_group()
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }
        self.assertRaises(RequestForbiddenException, submit_group_initial_model_controller, group_db_, group.get_id(), auth_json)

    def test_fail_not_authorized_user_2(self):
        group_db_ = InMemoryDBInterface()

        group = self._build_default_group()
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_1234567"
        }
        self.assertRaises(RequestForbiddenException, submit_group_initial_model_controller, group_db_, group.get_id(), auth_json)
