import unittest

from dependencies.python.fmlaas.controller.create_project import CreateProjectController
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor


class CreateProjectControllerTestCase(unittest.TestCase):

    def test_get_auth_conditions_pass(self):
        project_db = InMemoryDBInterface()

        project_name = "hello_world"
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = CreateProjectController(project_db, project_name, auth_context)

        auth_conditions = controller.get_auth_conditions()[0]

        self.assertEqual(len(auth_conditions), 1)
        self.assertEqual(auth_conditions[0], IsUser())

    def test_execute_pass(self):
        project_db = InMemoryDBInterface()

        project_name = "hello_world"
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        project_id = CreateProjectController(project_db, project_name, auth_context).execute()

        self.assertIsNotNone(project_id)

        loaded_project = DBObject.load_from_db(Project, project_id, project_db)

        self.assertEqual(loaded_project.get_id(), project_id)
        self.assertEqual(loaded_project.get_member_auth_level(
            "user_123442"), ProjectPrivilegeTypesEnum.OWNER)
