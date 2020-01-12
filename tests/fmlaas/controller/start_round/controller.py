import unittest

from dependencies.python.fmlaas.device_selection import RandomDeviceSelector
from dependencies.python.fmlaas.model import RoundConfiguration
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import Round
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.start_round import get_device_selector
from dependencies.python.fmlaas.controller.start_round import create_round
from dependencies.python.fmlaas.controller.start_round import start_round_controller

class StartRoundControllerTestCase(unittest.TestCase):

    def test_get_device_selector_pass(self):
        device_selector = get_device_selector(RoundConfiguration("5", "RANDOM"))

        self.assertEqual(device_selector.__class__, RandomDeviceSelector)

    def test_create_round_pass(self):
        devices = ["123", "234", "345", "3456"]
        round_config = RoundConfiguration("4", "RANDOM")

        round_builder = RoundBuilder()
        round_builder.set_id("round_test_id")
        round_builder.set_configuration(RoundConfiguration("1", "RANDOM").to_json())
        round_builder.set_start_model(Model("12312414", "1234/345345/12312414", "123211").to_json())
        round_builder.set_end_model(Model("1234", "1234/1234", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        new_round = create_round(devices, round.get_id(), round.get_end_model(), round_config)

        self.assertIsNotNone(new_round.get_id())
        self.assertEqual(new_round.get_devices(), devices)
        self.assertEqual(round_config.to_json(), new_round.get_configuration().to_json())
        self.assertEqual(new_round.get_previous_round_id(), round.get_id())

    def test_start_round_controller_pass_1(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()

        round_builder = RoundBuilder()
        round_builder.set_id("round_test_id")
        round_builder.set_configuration(RoundConfiguration("1", "RANDOM").to_json())
        round_builder.set_start_model(Model("12312414", "1234/345345/12312414", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        group.add_round(round)
        group.set_current_round_id(round.get_id())

        round.save_to_db(round_db)
        group.save_to_db(group_db)

        new_round_id = start_round_controller(round_db, group_db, group.get_id(), RoundConfiguration("1", "RANDOM"))
        new_round = DBObject.load_from_db(Round, new_round_id, round_db)
        previous_round = DBObject.load_from_db(Round, round.get_id(), round_db)
        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)

        self.assertEqual(new_round.get_previous_round_id(), round.get_id())
        self.assertEqual(new_round.get_start_model().to_json(), previous_round.get_end_model().to_json())
        self.assertEqual(new_round.get_devices(), ["34553"])

        self.assertEqual(updated_group.get_current_round_id(), new_round_id)
        self.assertTrue(updated_group.contains_round(new_round_id))

    def test_start_round_controller_pass_2(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.set_initial_model(Model("test_id", "test_id/test_id", "34532"))

        group.save_to_db(group_db)

        new_round_id = start_round_controller(round_db, group_db, group.get_id(), RoundConfiguration("1", "RANDOM"))
        new_round = DBObject.load_from_db(Round, new_round_id, round_db)
        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)

        self.assertEqual(new_round.get_previous_round_id(), "N/A")
        self.assertEqual(new_round.get_start_model().to_json(), updated_group.get_initial_model().to_json())
        self.assertEqual(new_round.get_devices(), ["34553"])

        self.assertEqual(updated_group.get_current_round_id(), new_round_id)
        self.assertTrue(updated_group.contains_round(new_round_id))
