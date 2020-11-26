from dependencies.python.fmlaas.controller.get_project import \
    GetProjectController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsUser)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class GetProjectControllerTestCase(AbstractTestCase):

    def test_execute_pass(self):
        db = InMemoryDBInterface()
        
        project = self._build_simple_project()
        project.save_to_db(db)

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = GetProjectController(db, project.id, auth_context)

        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)

        # Execute
        project_json = controller.execute()
        self.assertEqual(project.to_json(), project_json)
