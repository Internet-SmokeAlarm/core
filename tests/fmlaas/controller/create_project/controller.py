import unittest

from dependencies.python.fmlaas.controller.create_project import create_project_controller
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

class CreateProjectControllerTestCase(unittest.TestCase):

    def test_pass(self):
        db_ = InMemoryDBInterface()
        project_name = "hello_world"
        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user_123442"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        project_id = create_project_controller(db_, project_name, auth_context_processor)

        self.assertIsNotNone(project_id)

        loaded_project = DBObject.load_from_db(Project, project_id, db_)

        self.assertEqual(loaded_project.get_id(), project_id)
        self.assertEqual(loaded_project.get_member_auth_level("user_123442"), ProjectPrivilegeTypesEnum.OWNER)

    def test_fail(self):
        db_ = InMemoryDBInterface()
        project_name = "hello_world"
        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "device_123442"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, create_project_controller, db_, project_name, auth_context_processor)
