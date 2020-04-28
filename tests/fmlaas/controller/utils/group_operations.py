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
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.utils import update_round_path
from dependencies.python.fmlaas.utils import get_epoch_time
from dependencies.python.fmlaas.model.termination_criteria import DurationTerminationCriteria
from dependencies.python.fmlaas.controller.utils import termination_check

class GroupOperationsTestCase(unittest.TestCase):

    def test_update_round_path_pass(self):
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
        round_builder.set_configuration(RoundConfiguration(1, 0, "RANDOM", []).to_json())
        round_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())

        round.save_to_db(round_db)
        group.save_to_db(group_db)

        update_round_path(round, round_db, group_db)

        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)

        self.assertEqual(updated_group.get_current_round_ids(), [])
        self.assertTrue(updated_group.contains_round(round.get_id()))

    def test_update_round_path_pass_2(self):
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
        round_builder.set_configuration(RoundConfiguration(1, 0, "RANDOM", []).to_json())
        round_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()
        round.cancel()

        round_builder_2 = RoundBuilder()
        round_builder_2.set_id("round_test_id_2")
        round_builder_2.set_parent_group_id("test_id")
        round_builder_2.set_configuration(RoundConfiguration(1, 0, "RANDOM", []).to_json())
        round_builder_2.set_devices(["34553"])
        round_2 = round_builder_2.build()

        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.add_round_to_path_prev_id(round.get_id(), round_2.get_id())

        round.save_to_db(round_db)
        round_2.save_to_db(round_db)
        group.save_to_db(group_db)

        update_round_path(round, round_db, group_db)

        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)
        update_round_2 = DBObject.load_from_db(Round, round_2.get_id(), round_db)

        self.assertEqual(updated_group.get_current_round_ids(), [round_2.get_id()])
        self.assertTrue(update_round_2.is_in_progress())
        self.assertEqual(round.get_end_model().to_json(), update_round_2.get_start_model().to_json())
        self.assertTrue(updated_group.contains_round(round.get_id()))
        self.assertTrue(updated_group.contains_round(round_2.get_id()))

    def test_update_round_path_pass_3(self):
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
        round_builder.set_configuration(RoundConfiguration(1, 0, "RANDOM", []).to_json())
        round_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()
        round.cancel()

        round_builder_2 = RoundBuilder()
        round_builder_2.set_id("round_test_id_2")
        round_builder_2.set_parent_group_id("test_id")
        round_builder_2.set_configuration(RoundConfiguration(1, 0, "RANDOM", [DurationTerminationCriteria(100, 5000.123).to_json()]).to_json())
        round_builder_2.set_devices(["34553"])
        round_2 = round_builder_2.build()

        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.add_round_to_path_prev_id(round.get_id(), round_2.get_id())

        round.save_to_db(round_db)
        round_2.save_to_db(round_db)
        group.save_to_db(group_db)

        self.assertTrue(round_2.should_terminate())

        update_round_path(round, round_db, group_db)

        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)
        update_round_2 = DBObject.load_from_db(Round, round_2.get_id(), round_db)

        self.assertEqual(updated_group.get_current_round_ids(), [round_2.get_id()])
        self.assertTrue(update_round_2.is_in_progress())
        self.assertEqual(round.get_end_model().to_json(), update_round_2.get_start_model().to_json())
        self.assertTrue(updated_group.contains_round(round.get_id()))
        self.assertTrue(updated_group.contains_round(round_2.get_id()))
        self.assertFalse(update_round_2.should_terminate())

    def test_termination_check_pass(self):
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
        config = RoundConfiguration(1, 0, "RANDOM", [])
        config.add_termination_criteria(DurationTerminationCriteria(0, get_epoch_time()))
        round_builder.set_configuration(config.to_json())
        round_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        round_builder_2 = RoundBuilder()
        round_builder_2.set_id("round_test_id_2")
        round_builder_2.set_parent_group_id("test_id")
        round_builder_2.set_configuration(RoundConfiguration(1, 0, "RANDOM", []).to_json())
        round_builder_2.set_devices(["34553"])
        round_2 = round_builder_2.build()

        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.add_round_to_path_prev_id(round.get_id(), round_2.get_id())

        round.save_to_db(round_db)
        round_2.save_to_db(round_db)
        group.save_to_db(group_db)

        termination_check(round, round_db, group_db)

        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)
        update_round_2 = DBObject.load_from_db(Round, round_2.get_id(), round_db)

        self.assertEqual(updated_group.get_current_round_ids(), [round_2.get_id()])
        self.assertTrue(update_round_2.is_in_progress())
        self.assertEqual(round.get_end_model().to_json(), update_round_2.get_start_model().to_json())
        self.assertTrue(updated_group.contains_round(round.get_id()))
        self.assertTrue(updated_group.contains_round(round_2.get_id()))
        self.assertTrue(round.is_cancelled())

    def test_termination_check_pass_2(self):
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
        config = RoundConfiguration(1, 0, "RANDOM", [])
        config.add_termination_criteria(DurationTerminationCriteria(10, get_epoch_time()))
        round_builder.set_configuration(config.to_json())
        round_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        round_builder_2 = RoundBuilder()
        round_builder_2.set_id("round_test_id_2")
        round_builder_2.set_parent_group_id("test_id")
        round_builder_2.set_configuration(RoundConfiguration(1, 0, "RANDOM", []).to_json())
        round_builder_2.set_devices(["34553"])
        round_2 = round_builder_2.build()

        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.add_round_to_path_prev_id(round.get_id(), round_2.get_id())

        round.save_to_db(round_db)
        round_2.save_to_db(round_db)
        group.save_to_db(group_db)

        termination_check(round, round_db, group_db)

        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)
        update_round_2 = DBObject.load_from_db(Round, round_2.get_id(), round_db)

        self.assertEqual(updated_group.get_current_round_ids(), [round.get_id()])
        self.assertFalse(update_round_2.is_in_progress())
        self.assertTrue(updated_group.contains_round(round.get_id()))
        self.assertTrue(updated_group.contains_round(round_2.get_id()))
        self.assertTrue(round.is_in_progress())
