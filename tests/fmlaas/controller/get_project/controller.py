from dependencies.python.fmlaas.controller.get_project import get_project_controller
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobSequenceBuilder
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from ..abstract_controller_testcase import AbstractControllerTestCase


class GetProjectControllerTestCase(AbstractControllerTestCase):

    def _build_default_project(self):
        project_builder = ProjectBuilder()
        project_builder.set_id("test_id")
        project_builder.set_name("test_name")

        return project_builder.build()

    def test_pass_simple(self):
        db = InMemoryDBInterface()
        project = self._build_default_project()
        project.add_or_update_member(
            "user123", ProjectPrivilegeTypesEnum.ADMIN)
        project.save_to_db(db)

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user123"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        project_json = get_project_controller(
            db, project.get_id(), auth_context_processor)

        self.assertEqual(project_json,
                         {'name': 'test_name',
                          'ID': 'test_id',
                          'devices': {},
                             'job_sequences': {},
                             'members': {'user123': {'permission_level': 10}},
                             "billing": {}})

    def test_not_authorized_1(self):
        db = InMemoryDBInterface()
        project = self._build_default_project()
        project.add_or_update_member(
            "user123", ProjectPrivilegeTypesEnum.ADMIN)
        project.save_to_db(db)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "user123"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(
            RequestForbiddenException,
            get_project_controller,
            db,
            project.get_id(),
            auth_context_processor)

    def test_not_authorized_2(self):
        db = InMemoryDBInterface()
        project = self._build_default_project()
        project.add_or_update_member(
            "user123", ProjectPrivilegeTypesEnum.ADMIN)
        project.save_to_db(db)

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user1234"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(
            RequestForbiddenException,
            get_project_controller,
            db,
            project.get_id(),
            auth_context_processor)
