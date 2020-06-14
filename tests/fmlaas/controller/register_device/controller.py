import unittest

from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import ApiKey
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.register_device import RegisterDeviceController
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions import HasProjectPermissions
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from ..abstract_testcase import AbstractTestCase


class RegisterDeviceControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        project = self._build_simple_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        id, key_plaintext = RegisterDeviceController(project_db_,
                                                     key_db_,
                                                     project.get_id(),
                                                     auth_context).execute()
        self.assertIsNotNone(id)
        self.assertIsNotNone(key_plaintext)
        self.assertEqual(
            id, DBObject.load_from_db(
                ApiKey, id, key_db_).get_id())

    def test_load_data_pass(self):
        project_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        project = self._build_simple_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = RegisterDeviceController(project_db_,
                                              key_db_,
                                              project.get_id(),
                                              auth_context)
        controller.load_data()

        self.assertEqual(controller.project, project)

    def test_get_auth_conditions_pass(self):
        project_db_ = InMemoryDBInterface()
        key_db_ = InMemoryDBInterface()

        project = self._build_simple_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = RegisterDeviceController(project_db_,
                                              key_db_,
                                              project.get_id(),
                                              auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()

        self.assertEqual(len(auth_conditions), 1)

        self.assertEqual(len(auth_conditions[0]), 2)
        self.assertEqual(auth_conditions[0][0], IsUser())
        self.assertEqual(auth_conditions[0][1], HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_WRITE))
