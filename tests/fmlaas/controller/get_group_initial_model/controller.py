import unittest
import os

from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.get_group_initial_model import get_group_initial_model_controller

class GetGroupInitialModelControllerTestCase(unittest.TestCase):

    def _build_default_group(self):
        group_builder = GroupBuilder()
        group_builder.set_id("test_id")
        group_builder.set_name("test_name")

        group = group_builder.build()
        group.add_device("12344")
        group.add_round("1234432414")
        group.set_current_round_id("1234432414")
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.READ_ONLY)

        return group

    def test_pass_1(self):
        db_ = InMemoryDBInterface()
        group = self._build_default_group()
        group.save_to_db(db_)

        os.environ["MODELS_BUCKET"] = "test123"

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        is_initial_model_set, presigned_url = get_group_initial_model_controller(db_, group.get_id(), auth_json)
        self.assertFalse(is_initial_model_set)

    def test_pass_2(self):
        db_ = InMemoryDBInterface()
        group = self._build_default_group()
        group.set_initial_model(Model("34534534234", "12344/1231231243245/34534534234", "233423"))
        group.save_to_db(db_)

        os.environ["MODELS_BUCKET"] = "test123"

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        is_initial_model_set, presigned_url = get_group_initial_model_controller(db_, group.get_id(), auth_json)
        self.assertTrue(is_initial_model_set)
        self.assertIsNotNone(presigned_url)

    def test_fail_unauthorized_1(self):
        db_ = InMemoryDBInterface()
        group = self._build_default_group()
        group.save_to_db(db_)

        os.environ["MODELS_BUCKET"] = "test123"

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "user_12345"
        }
        self.assertRaises(RequestForbiddenException, get_group_initial_model_controller, db_, group.get_id(), auth_json)

    def test_fail_unauthorized_2(self):
        db_ = InMemoryDBInterface()
        group = self._build_default_group()
        group.save_to_db(db_)

        os.environ["MODELS_BUCKET"] = "test123"

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }
        self.assertRaises(RequestForbiddenException, get_group_initial_model_controller, db_, group.get_id(), auth_json)
