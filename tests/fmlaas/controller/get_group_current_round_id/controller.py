import unittest

from dependencies.python.fmlaas.controller.get_group_current_round_id import get_group_current_round_id_controller
from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum

class GetGroupCurrentRoundIdControllerTestCase(unittest.TestCase):

    def _build_default_group(self):
        group_builder = GroupBuilder()
        group_builder.set_id("test_id")
        group_builder.set_name("test_name")

        group = group_builder.build()
        group.add_device("12344")
        group.create_round_path("1234432414")
        group.add_current_round_id("1234432414")
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.OWNER)

        return group

    def test_pass(self):
        db_ = InMemoryDBInterface()
        group = self._build_default_group()
        group.save_to_db(db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "12344"
        }
        current_round_id = get_group_current_round_id_controller(db_, group.get_id(), auth_json)
        self.assertEqual("1234432414", current_round_id[0])

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        current_round_id_2 = get_group_current_round_id_controller(db_, group.get_id(), auth_json)
        self.assertEqual("1234432414", current_round_id_2[0])

    def test_not_authorized_1(self):
        db_ = InMemoryDBInterface()
        group = self._build_default_group()
        group.save_to_db(db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "34"
        }
        self.assertRaises(RequestForbiddenException, get_group_current_round_id_controller, db_, group.get_id(), auth_json)

    def test_not_authorized_2(self):
        db_ = InMemoryDBInterface()
        group = self._build_default_group()
        group.save_to_db(db_)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_1234"
        }
        self.assertRaises(RequestForbiddenException, get_group_current_round_id_controller, db_, group.get_id(), auth_json)
