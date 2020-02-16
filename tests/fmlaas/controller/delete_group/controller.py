import unittest

from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.controller.delete_group import delete_group_controller
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import Round
from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import RoundConfiguration
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum

class DeleteGroupControllerTestCase(unittest.TestCase):

    def _build_default_group(self):
        group_builder = GroupBuilder()
        group_builder.set_id("test_id")
        group_builder.set_name("test_name")

        return group_builder.build()

    def _build_default_round(self):
        round_builder = RoundBuilder()
        round_builder.set_id("2345")
        round_builder.set_parent_group_id("test_id")
        configuration = RoundConfiguration("1", "RANDOM")
        round_builder.set_configuration(configuration.to_json())
        round_builder.set_devices(["3456"])
        round_builder.set_start_model(Model("1234", "1234/1234", "123211").to_json())

        return round_builder.build()

    def test_pass_1(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        group = self._build_default_group()
        round = self._build_default_round()
        group.create_round_path("2345")
        group.add_or_update_member("user12344", GroupPrivilegeTypesEnum.OWNER)
        group.save_to_db(group_db)
        round.save_to_db(round_db)

        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user12344"
        }

        delete_group_controller(group_db, round_db, group.get_id(), auth_json)

        self.assertRaises(KeyError, DBObject.load_from_db, FLGroup, group.get_id(), group_db)
        self.assertRaises(KeyError, DBObject.load_from_db, Round, round.get_id(), round_db)

    def test_fail_group_nonexistant(self):
        pass

    def test_fail_device_not_authorized(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        group = self._build_default_group()
        round = self._build_default_round()
        group.create_round_path("2345")
        group.add_or_update_member("user12344", GroupPrivilegeTypesEnum.OWNER)
        group.save_to_db(group_db)
        round.save_to_db(round_db)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "user12344"
        }

        self.assertRaises(RequestForbiddenException, delete_group_controller, group_db, round_db, group.get_id(), auth_json)

    def test_fail_not_authorized_to_access_group(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        group = self._build_default_group()
        round = self._build_default_round()
        group.create_round_path("2345")
        group.add_or_update_member("user12344", GroupPrivilegeTypesEnum.OWNER)
        group.save_to_db(group_db)
        round.save_to_db(round_db)

        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user123445"
        }

        self.assertRaises(RequestForbiddenException, delete_group_controller, group_db, round_db, group.get_id(), auth_json)
