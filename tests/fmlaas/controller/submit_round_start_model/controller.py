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
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.submit_round_start_model import submit_round_start_model_controller
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

class SubmitRoundStartModelControllerTestCase(unittest.TestCase):

    def _build_default_group(self):
        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        group = builder.build()

        group.add_device("12312313123")
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)
        group.add_or_update_member("user_123456", GroupPrivilegeTypesEnum.READ_ONLY)

        return group

    def _build_default_round(self, id):
        round_builder = RoundBuilder()
        round_builder.set_id(id)
        round_builder.set_parent_group_id("test_id")
        round_builder.set_configuration(RoundConfiguration(1, 0, "RANDOM", []).to_json())
        round_builder.set_devices(["34553"])
        round = round_builder.build()

        return round

    def test_pass(self):
        round_db = InMemoryDBInterface()
        group_db = InMemoryDBInterface()

        group = self._build_default_group()
        round = self._build_default_round("round_test_id")

        group.save_to_db(group_db)
        round.save_to_db(round_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        can_submit_start_model, presigned_url = submit_round_start_model_controller(group_db, round_db, round.get_id(), auth_context_processor)

        self.assertTrue(can_submit_start_model)
        self.assertIsNotNone(presigned_url)

    def test_fail_not_authorized_user(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        group = self._build_default_group()
        round = self._build_default_round("round_test_id")

        group.save_to_db(group_db)
        round.save_to_db(round_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, submit_round_start_model_controller, group_db, round_db, "round_test_id", auth_context_processor)

    def test_fail_not_authorized_device(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        group = self._build_default_group()
        round = self._build_default_round("round_test_id")

        group.save_to_db(group_db)
        round.save_to_db(round_db)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "34553"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, submit_round_start_model_controller, group_db, round_db, "round_test_id", auth_context_processor)

    def test_fail_not_authorized_round(self):
        group_db = InMemoryDBInterface()
        round_db = InMemoryDBInterface()

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, submit_round_start_model_controller, round_db, group_db, "woot", auth_context_processor)
