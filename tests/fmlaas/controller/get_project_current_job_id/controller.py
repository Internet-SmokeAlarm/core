import unittest

from dependencies.python.fmlaas.controller.get_project_current_job_id import get_project_current_job_id_controller
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

class GetProjectCurrentJobIdControllerTestCase(unittest.TestCase):

    def _build_default_project(self):
        project_builder = ProjectBuilder()
        project_builder.set_id("test_id")
        project_builder.set_name("test_name")

        project = project_builder.build()
        project.add_device("12344")
        project.create_job_path("1234432414")
        project.add_current_job_id("1234432414")
        project.add_or_update_member("user_12345", ProjectPrivilegeTypesEnum.OWNER)

        return project

    def test_pass(self):
        db_ = InMemoryDBInterface()
        project = self._build_default_project()
        project.save_to_db(db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "12344"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        current_job_id = get_project_current_job_id_controller(db_, project.get_id(), auth_context_processor)
        self.assertEqual("1234432414", current_job_id[0])

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        current_job_id_2 = get_project_current_job_id_controller(db_, project.get_id(), auth_context_processor)
        self.assertEqual("1234432414", current_job_id_2[0])

    def test_not_authorized_1(self):
        db_ = InMemoryDBInterface()
        project = self._build_default_project()
        project.save_to_db(db_)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "34"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        self.assertRaises(RequestForbiddenException, get_project_current_job_id_controller, db_, project.get_id(), auth_context_processor)

    def test_not_authorized_2(self):
        db_ = InMemoryDBInterface()
        project = self._build_default_project()
        project.save_to_db(db_)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_1234"
        }
        auth_context_processor = AuthContextProcessor(auth_json)
        self.assertRaises(RequestForbiddenException, get_project_current_job_id_controller, db_, project.get_id(), auth_context_processor)
