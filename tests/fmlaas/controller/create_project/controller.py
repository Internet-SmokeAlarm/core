from ..abstract_testcase import AbstractTestCase
from dependencies.python.fmlaas.controller.create_project import CreateProjectController
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.model import User
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor


class CreateProjectControllerTestCase(AbstractTestCase):

    def test_get_auth_conditions_pass(self):
        project_db = InMemoryDBInterface()
        user_db = InMemoryDBInterface()

        user = self._create_empty_user()
        user.user.save_to_db(user_db)

        project_name = "hello_world"
        project_description = "test description"
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": user.username
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = CreateProjectController(project_db,
                                             user_db,
                                             project_name,
                                             project_description,
                                             auth_context)

        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser()
            ]
        ]

        self.assertEqual(auth_conditions, correct_auth_conditions)

    def test_execute_pass(self):
        project_db = InMemoryDBInterface()
        user_db = InMemoryDBInterface()

        user = self._create_empty_user()
        user.user.save_to_db(user_db)

        project_name = "hello_world"
        project_description = "test description"
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": user.username
        }
        auth_context = AuthContextProcessor(auth_json)

        project = CreateProjectController(project_db,
                                          user_db,
                                          project_name,
                                          project_description,
                                          auth_context).execute()

        self.assertIsNotNone(project)

        loaded_project = DBObject.load_from_db(Project, project.get_id(), project_db)

        self.assertEqual(loaded_project.get_id(), project.get_id())
        self.assertEqual(loaded_project.description, project.description)
        self.assertEqual(loaded_project.get_member_auth_level(
            user.username), ProjectPrivilegeTypesEnum.OWNER)
        self.assertEqual(DBObject.load_from_db(User, user.username, user_db).projects[0]["name"], project_name)
