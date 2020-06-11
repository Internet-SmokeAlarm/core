from dependencies.python.fmlaas.controller.get_project import GetProjectController
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobSequenceBuilder
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions import HasProjectPermissions
from ..abstract_controller_testcase import AbstractControllerTestCase


class GetProjectControllerTestCase(AbstractControllerTestCase):

    def test_execute_pass(self):
        db = InMemoryDBInterface()
        project = self._build_simple_project()
        project.save_to_db(db)

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        project_json = GetProjectController(
            db, project.get_id(), auth_context).execute()

        self.assertEqual(project.to_json(), project_json)

    def test_load_data(self):
        db = InMemoryDBInterface()
        project = self._build_simple_project()
        project.save_to_db(db)

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = GetProjectController(db, project.get_id(), auth_context)
        controller.load_data()

        self.assertEqual(controller.project, project)

    def test_get_auth_conditions(self):
        db = InMemoryDBInterface()
        project = self._build_simple_project()
        project.save_to_db(db)

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = GetProjectController(db, project.get_id(), auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()[0]

        self.assertEqual(len(auth_conditions), 2)
        self.assertEqual(auth_conditions[0], IsUser())
        self.assertEqual(auth_conditions[1], HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_ONLY))
