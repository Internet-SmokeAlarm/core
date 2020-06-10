import unittest

from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import ApiKey
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.register_device import register_device_controller
from dependencies.python.fmlaas.request_processor import AuthContextProcessor


class RegisterDeviceControllerTestCase(unittest.TestCase):

    def _build_default_project(self):
        project_builder = ProjectBuilder()
        project_builder.set_id("test_id")
        project_builder.set_name("test_name")

        project = project_builder.build()
        project.add_device("12344")
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)
        project.add_or_update_member(
            "user_123456", ProjectPrivilegeTypesEnum.READ_ONLY)

        return project

    def test_pass(self):
        project_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        project = self._build_default_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        id, key_plaintext = register_device_controller(project_db_,
                                                       key_db_,
                                                       project.get_id(),
                                                       auth_context)
        self.assertIsNotNone(id)
        self.assertIsNotNone(key_plaintext)
        self.assertEqual(
            id, DBObject.load_from_db(
                ApiKey, id, key_db_).get_id())

    def test_fail_not_authorized_user(self):
        project_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        project = self._build_default_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_123456"
        }
        auth_context = AuthContextProcessor(auth_json)
        self.assertRaises(
            RequestForbiddenException,
            register_device_controller,
            project_db_,
            key_db_,
            project.get_id(),
            auth_context)

    def test_fail_not_authorized_user_2(self):
        project_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        project = self._build_default_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_1234567"
        }
        auth_context = AuthContextProcessor(auth_json)
        self.assertRaises(
            RequestForbiddenException,
            register_device_controller,
            project_db_,
            key_db_,
            project.get_id(),
            auth_context)

    def test_fail_not_authorized_device(self):
        project_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        project = self._build_default_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        self.assertRaises(
            RequestForbiddenException,
            register_device_controller,
            project_db_,
            key_db_,
            project.get_id(),
            auth_context)
