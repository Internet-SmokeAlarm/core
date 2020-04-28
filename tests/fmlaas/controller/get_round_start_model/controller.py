import unittest

from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import RoundConfiguration
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.get_round_start_model import get_round_start_model_controller
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

class GetRoundStartModelControllerTestCase(unittest.TestCase):

    def _build_default_group(self):
        group_builder = GroupBuilder()
        group_builder.set_id("test_id")
        group_builder.set_name("test_name")

        group = group_builder.build()
        group.add_device("12344")
        group.create_round_path("1234432414")
        group.add_current_round_id("1234432414")
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.READ_ONLY)

        return group

    def _build_default_round(self):
        round_builder = RoundBuilder()
        round_builder.set_id("round_test_id")
        round_builder.set_parent_group_id("test_id")
        round_builder.set_configuration(RoundConfiguration(1, 0, "RANDOM", []).to_json())
        round_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        round_builder.set_aggregate_model(Model("1234", "1234/aggregate_model", "123211").to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        return round

    def test_pass_1(self):
        group_db_ = InMemoryDBInterface()
        round_db_ = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(round_db_)

        group = self._build_default_group()
        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        presigned_url = get_round_start_model_controller(group_db_,
                                                         round_db_,
                                                         group.get_id(),
                                                         round.get_id(),
                                                         auth_context_processor)
        self.assertIsNotNone(presigned_url)

    def test_pass_2(self):
        group_db_ = InMemoryDBInterface()
        round_db_ = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(round_db_)

        group = self._build_default_group()
        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "34553"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        presigned_url = get_round_start_model_controller(group_db_,
                                                         round_db_,
                                                         group.get_id(),
                                                         round.get_id(),
                                                         auth_context_processor)
        self.assertIsNotNone(presigned_url)

    def test_fail_not_authorized_1(self):
        group_db_ = InMemoryDBInterface()
        round_db_ = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(round_db_)

        group = self._build_default_group()
        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "123445"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        self.assertRaises(RequestForbiddenException, get_round_start_model_controller, group_db_, round_db_, group.get_id(), round.get_id(), auth_context_processor)

    def test_fail_not_authorized_2(self):
        group_db_ = InMemoryDBInterface()
        round_db_ = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(round_db_)

        group = self._build_default_group()
        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "123445"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        self.assertRaises(RequestForbiddenException, get_round_start_model_controller, group_db_, round_db_, group.get_id(), round.get_id(), auth_context_processor)

    def test_fail_not_authorized_3(self):
        group_db_ = InMemoryDBInterface()
        round_db_ = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(round_db_)

        group = self._build_default_group()
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "12344"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        self.assertRaises(RequestForbiddenException, get_round_start_model_controller, group_db_, round_db_, group.get_id(), round.get_id(), auth_context_processor)

    def test_fail_not_authorized_4(self):
        group_db_ = InMemoryDBInterface()
        round_db_ = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(round_db_)

        group = self._build_default_group()
        group.create_round_path(round.get_id())
        group.add_current_round_id(round.get_id())
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "12344"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        self.assertRaises(RequestForbiddenException, get_round_start_model_controller, group_db_, round_db_, group.get_id(), round.get_id(), auth_context_processor)
