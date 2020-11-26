from dependencies.python.fmlaas.controller.create_project import \
    CreateProjectController
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import (DBObject, Project,
                                              ProjectPrivilegeTypesEnum, User)
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class CreateProjectControllerTestCase(AbstractTestCase):

    def test_pass(self):
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

        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser()
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)

        # Execute
        project = controller.execute()
        self.assertIsNotNone(project)

        loaded_project = DBObject.load_from_db(Project, project.id, project_db)

        self.assertEqual(loaded_project.id, project.id)
        self.assertEqual(loaded_project.description, project.description)
        self.assertEqual(loaded_project.get_member_auth_level(
            user.username), ProjectPrivilegeTypesEnum.OWNER)
        self.assertEqual(DBObject.load_from_db(User, user.username, user_db).projects[0]["name"], project_name)
