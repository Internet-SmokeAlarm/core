import unittest

from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsDevice
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsReadOnlyProjectEntity
from ....abstract_controller_testcase import AbstractControllerTestCase


class IsReadOnlyProjectEntityTestCase(AbstractControllerTestCase):

    def test_verify_pass_false(self):
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        project = self._build_simple_project()

        self.assertFalse(IsReadOnlyProjectEntity(project).verify(auth_context))

    def test_verify_pass_true(self):
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        project = self._build_simple_project()

        self.assertTrue(IsReadOnlyProjectEntity(project).verify(auth_context))

    def test_eq_pass(self):
        project = self._build_simple_project()

        self.assertTrue(IsReadOnlyProjectEntity(project) == IsReadOnlyProjectEntity(project))

    def test_eq_fail(self):
        project = self._build_simple_project()

        project_2 = self._build_simple_project()
        project_2.add_or_update_job_sequence(self._build_simple_job_sequence())

        self.assertFalse(IsReadOnlyProjectEntity(project) == IsReadOnlyProjectEntity(project_2))

    def test_eq_fail_2(self):
        project = self._build_simple_project()

        self.assertFalse(IsReadOnlyProjectEntity(project) == IsDevice())
