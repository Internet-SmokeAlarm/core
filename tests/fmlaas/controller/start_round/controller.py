import unittest

from dependencies.python.fmlaas.device_selection import RandomDeviceSelector
from dependencies.python.fmlaas.model import RoundConfiguration
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import Round
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.start_round import get_device_selector
from dependencies.python.fmlaas.controller.start_round import create_round
from dependencies.python.fmlaas.controller.start_round import start_round_controller

class StartRoundControllerTestCase(unittest.TestCase):

    def test_get_device_selector_pass(self):
        device_selector = get_device_selector(RoundConfiguration("5", "RANDOM", []))

        self.assertEqual(device_selector.__class__, RandomDeviceSelector)

    def test_create_round_pass(self):
        devices = ["123", "234", "345", "3456"]
        round_config = RoundConfiguration("4", "RANDOM", [])

        new_round = create_round(devices, "test_id123", round_config)

        self.assertIsNotNone(new_round.get_id())
        self.assertEqual(new_round.get_devices(), devices)
        self.assertEqual(new_round.get_parent_group_id(), "test_id123")
        self.assertEqual(round_config.to_json(), new_round.get_configuration().to_json())

    def test_start_round_controller_pass_1(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)

        round_builder = RoundBuilder()
        round_builder.set_id("round_test_id")
        round_builder.set_parent_group_id("test_id")
        round_builder.set_configuration(RoundConfiguration("1", "RANDOM", []).to_json())
        round_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())

        round.save_to_db(round_db)
        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }

        new_round_id = start_round_controller(round_db, group_db, group.get_id(), RoundConfiguration("1", "RANDOM", []), round.get_id(), auth_json)
        new_round = DBObject.load_from_db(Round, new_round_id, round_db)

        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)

        self.assertEqual(updated_group.get_current_round_ids(), [round.get_id()])
        self.assertTrue(updated_group.contains_round(new_round_id))

    def test_start_round_controller_pass_2(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)

        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }

        new_round_id = start_round_controller(round_db, group_db, group.get_id(), RoundConfiguration("1", "RANDOM", []), None, auth_json)
        new_round = DBObject.load_from_db(Round, new_round_id, round_db)
        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)

        self.assertEqual(new_round.get_devices(), ["34553"])

        self.assertEqual(updated_group.get_current_round_ids(), [new_round_id])
        self.assertEqual(updated_group.get_round_paths(), [[new_round_id]])
        self.assertTrue(updated_group.contains_round(new_round_id))

    def test_start_round_controller_fail(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)
        group.add_or_update_member("user_123456", GroupPrivilegeTypesEnum.READ_ONLY)

        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }

        self.assertRaises(RequestForbiddenException, start_round_controller, round_db, group_db, group.get_id(), RoundConfiguration("1", "RANDOM", []), None, auth_json)

    def test_start_round_controller_fail_2(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)
        group.add_or_update_member("user_123456", GroupPrivilegeTypesEnum.READ_ONLY)

        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_1234567"
        }

        self.assertRaises(RequestForbiddenException, start_round_controller, round_db, group_db, group.get_id(), RoundConfiguration("1", "RANDOM", []), None, auth_json)

    def test_start_round_controller_fail_3(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)
        group.add_or_update_member("user_123456", GroupPrivilegeTypesEnum.READ_ONLY)

        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "34553"
        }

        self.assertRaises(RequestForbiddenException, start_round_controller, round_db, group_db, group.get_id(), RoundConfiguration("1", "RANDOM", []), None, auth_json)
