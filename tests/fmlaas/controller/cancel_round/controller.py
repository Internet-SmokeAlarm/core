import unittest

from dependencies.python.fmlaas.model import RoundConfiguration
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import Round
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.model import RoundStatus
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.cancel_round import cancel_round_controller

class CancelRoundControllerTestCase(unittest.TestCase):

    def test_pass(self):
        round_db = InMemoryDBInterface()
        group_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        group = builder.build()
        group.add_device("12312313123")
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        round_builder = RoundBuilder()
        round_builder.set_id("round_test_id")
        round_builder.set_parent_group_id("test_id")
        round_builder.set_configuration(RoundConfiguration("1", "RANDOM", []).to_json())
        round_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())

        group.save_to_db(group_db)
        round.save_to_db(round_db)

        cancel_round_controller(group_db, round_db, round.get_id(), auth_context_processor)

        db_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)
        db_round = DBObject.load_from_db(Round, round.get_id(), round_db)

        self.assertTrue(db_round.is_cancelled())
        self.assertTrue(round.get_id() not in db_group.get_current_round_ids())
        self.assertEqual(0, len(db_group.get_current_round_ids()))

    def test_pass_2(self):
        round_db = InMemoryDBInterface()
        group_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        group = builder.build()
        group.add_device("12312313123")
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        round_builder = RoundBuilder()
        round_builder.set_id("round_test_id")
        round_builder.set_parent_group_id("test_id")
        round_builder.set_configuration(RoundConfiguration("1", "RANDOM", []).to_json())
        round_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        round_builder = RoundBuilder()
        round_builder.set_id("round_test_id_2")
        round_builder.set_parent_group_id("test_id")
        round_builder.set_configuration(RoundConfiguration("1", "RANDOM", []).to_json())
        round_builder.set_devices(["34553"])
        round_2 = round_builder.build()

        round_builder = RoundBuilder()
        round_builder.set_id("round_test_id_3")
        round_builder.set_parent_group_id("test_id")
        round_builder.set_configuration(RoundConfiguration("1", "RANDOM", []).to_json())
        round_builder.set_devices(["34553"])
        round_3 = round_builder.build()
        round_3.cancel()

        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.add_round_to_path_prev_id(round.get_id(), round_3.get_id())
        group.add_round_to_path_prev_id(round_3.get_id(), round_2.get_id())

        group.save_to_db(group_db)
        round.save_to_db(round_db)
        round_2.save_to_db(round_db)
        round_3.save_to_db(round_db)

        cancel_round_controller(group_db, round_db, round.get_id(), auth_context_processor)

        db_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)
        db_round = DBObject.load_from_db(Round, round.get_id(), round_db)
        db_round_2 = DBObject.load_from_db(Round, round_2.get_id(), round_db)

        self.assertTrue(db_round.is_cancelled())
        self.assertTrue(round.get_id() not in db_group.get_current_round_ids())
        self.assertEqual(1, len(db_group.get_current_round_ids()))
        self.assertTrue(round_2.get_id() in db_group.get_current_round_ids())
        self.assertEqual(db_round_2.get_status(), RoundStatus.IN_PROGRESS)
        self.assertEqual(db_round_2.get_start_model().to_json(), db_round.get_start_model().to_json())

    def test_fail_not_authorized_user(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)
        group.add_or_update_member("user_123456", GroupPrivilegeTypesEnum.READ_ONLY)

        round_builder = RoundBuilder()
        round_builder.set_id("round_test_id")
        round_builder.set_parent_group_id("test_id")
        round_builder.set_configuration(RoundConfiguration("1", "RANDOM", []).to_json())
        round_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        group.save_to_db(group_db)
        round.save_to_db(round_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, cancel_round_controller, group_db, round_db, "round_test_id", auth_context_processor)

    def test_fail_not_authorized_device(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)
        group.add_or_update_member("user_123456", GroupPrivilegeTypesEnum.READ_ONLY)

        round_builder = RoundBuilder()
        round_builder.set_id("round_test_id")
        round_builder.set_parent_group_id("test_id")
        round_builder.set_configuration(RoundConfiguration("1", "RANDOM", []).to_json())
        round_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        group.save_to_db(group_db)
        round.save_to_db(round_db)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "34553"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, cancel_round_controller, group_db, round_db, "round_test_id", auth_context_processor)

    def test_fail_not_authorized(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, cancel_round_controller, round_db, group_db, "woot", auth_context_processor)
