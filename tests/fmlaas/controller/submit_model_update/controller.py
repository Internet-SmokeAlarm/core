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
from dependencies.python.fmlaas.controller.submit_model_update import submit_model_update_controller

class SubmitModelUpdateControllerTestCase(unittest.TestCase):

    def _build_default_group(self):
        group_builder = GroupBuilder()
        group_builder.set_id("test_id")
        group_builder.set_name("test_name")

        group = group_builder.build()
        group.add_device("12344")
        group.add_round("1234432414")
        group.set_current_round_id("1234432414")
        group.add_or_update_member("user_123456", GroupPrivilegeTypesEnum.OWNER)

        return group

    def _build_default_round(self):
        round_builder = RoundBuilder()
        round_builder.set_id("round_test_id")
        round_builder.set_configuration(RoundConfiguration("1", "RANDOM").to_json())
        round_builder.set_start_model(Model("12312414", "1234/345345/12312414", "123211").to_json())
        round_builder.set_end_model(Model("1234", "1234/1234", "123211").to_json())
        round_builder.set_devices(["12344"])
        round = round_builder.build()

        return round

    def test_pass(self):
        group_db_ = InMemoryDBInterface()
        round_db_ = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(round_db_)

        group = self._build_default_group()
        group.add_round(round.get_id())
        group.set_current_round_id(round.get_id())
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "12344"
        }
        can_submit_model_to_round, presigned_url = submit_model_update_controller(group_db_,
                                                                                  round_db_,
                                                                                  group.get_id(),
                                                                                  round.get_id(),
                                                                                  auth_json)
        self.assertTrue(can_submit_model_to_round)
        self.assertIsNotNone(presigned_url)

    def test_fail_not_authorized_user(self):
        group_db_ = InMemoryDBInterface()
        round_db_ = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(round_db_)

        group = self._build_default_group()
        group.add_round(round.get_id())
        group.set_current_round_id(round.get_id())
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }
        self.assertRaises(RequestForbiddenException, submit_model_update_controller, group_db_, round_db_, group.get_id(), round.get_id(), auth_json)

    def test_fail_not_authorized_device(self):
        group_db_ = InMemoryDBInterface()
        round_db_ = InMemoryDBInterface()

        round = self._build_default_round()
        round.save_to_db(round_db_)

        group = self._build_default_group()
        group.add_round(round.get_id())
        group.set_current_round_id(round.get_id())
        group.save_to_db(group_db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "123445"
        }
        self.assertRaises(RequestForbiddenException, submit_model_update_controller, group_db_, round_db_, group.get_id(), round.get_id(), auth_json)

    def test_fail_not_authorized_round(self):
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
        self.assertRaises(RequestForbiddenException, submit_model_update_controller, group_db_, round_db_, group.get_id(), round.get_id(), auth_json)
