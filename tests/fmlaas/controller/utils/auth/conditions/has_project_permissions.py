import unittest

from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsDevice)
from dependencies.python.fmlaas.model import (ProjectFactory,
                                              ProjectPrivilegeTypesEnum)
from dependencies.python.fmlaas.request_processor import AuthContextProcessor


class HasProjectPermissionsTestCase(unittest.TestCase):

    def _build_project(self):
        project = ProjectFactory.create_project("test_id",
                                                "test_name")
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.OWNER)

        return project

    def test_verify_pass_false(self):
        project = self._build_project()

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertFalse(HasProjectPermissions(project, ProjectPrivilegeTypesEnum.OWNER).verify(auth_context))

    def test_verify_pass_true(self):
        project = self._build_project()

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_12344"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertTrue(HasProjectPermissions(project, ProjectPrivilegeTypesEnum.OWNER).verify(auth_context))

    def test_eq_pass(self):
        project = self._build_project()

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12344"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertTrue(HasProjectPermissions(project, ProjectPrivilegeTypesEnum.OWNER) == HasProjectPermissions(project, ProjectPrivilegeTypesEnum.OWNER))

    def test_eq_fail_type(self):
        project = self._build_project()

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12344"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertFalse(HasProjectPermissions(project, ProjectPrivilegeTypesEnum.ADMIN) == IsDevice())

    def test_eq_fail_data(self):
        project = self._build_project()

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12344"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertFalse(HasProjectPermissions(project, ProjectPrivilegeTypesEnum.ADMIN) == HasProjectPermissions(project, ProjectPrivilegeTypesEnum.OWNER))
