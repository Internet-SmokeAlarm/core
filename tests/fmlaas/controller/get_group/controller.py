import unittest

from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.controller.get_group import get_group_controller
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum

class GetGroupControllerTestCase(unittest.TestCase):

    def _build_default_group(self):
        group_builder = GroupBuilder()
        group_builder.set_id("test_id")
        group_builder.set_name("test_name")

        return group_builder.build()

    def test_pass(self):
        db = InMemoryDBInterface()
        group = self._build_default_group()
        group.add_or_update_member("user123", GroupPrivilegeTypesEnum.ADMIN)
        group.save_to_db(db)

        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user123"
        }

        group_json = get_group_controller(db, group.get_id(), auth_json)

        self.assertEqual(group_json, {'name': 'test_name', 'ID': 'test_id', 'devices': {}, 'rounds': {}, 'current_round_id': 'N/A', 'initial_model': {}, 'members': {'user123': {'permission_level': 10}}, 'is_initial_model_set': False})

    def test_not_authorized_1(self):
        db = InMemoryDBInterface()
        group = self._build_default_group()
        group.add_or_update_member("user123", GroupPrivilegeTypesEnum.ADMIN)
        group.save_to_db(db)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "user123"
        }

        self.assertRaises(RequestForbiddenException, get_group_controller, db, group.get_id(), auth_json)

    def test_not_authorized_2(self):
        db = InMemoryDBInterface()
        group = self._build_default_group()
        group.add_or_update_member("user123", GroupPrivilegeTypesEnum.ADMIN)
        group.save_to_db(db)

        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user1234"
        }

        self.assertRaises(RequestForbiddenException, get_group_controller, db, group.get_id(), auth_json)