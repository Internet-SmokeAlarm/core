import unittest

from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsDevice
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsDevice
from ....abstract_testcase import AbstractTestCase


class ProjectContainsDeviceTestCase(AbstractTestCase):

    def test_verify_pass_false(self):
        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        project = self._build_simple_project()

        self.assertFalse(ProjectContainsDevice(project).verify(auth_context))

    def test_verify_pass_true(self):
        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)

        project = self._build_simple_project()

        self.assertTrue(ProjectContainsDevice(project).verify(auth_context))

    def test_eq_pass(self):
        project = self._build_simple_project()

        self.assertEqual(ProjectContainsDevice(project), ProjectContainsDevice(project))

    def test_eq_fail(self):
        project = self._build_simple_project()
        project_2 = self._build_simple_project()
        project_2.add_or_update_job_sequence(self._build_simple_job_sequence())

        self.assertNotEqual(ProjectContainsDevice(project), ProjectContainsDevice(project_2))

    def test_eq_fail_2(self):
        project = self._build_simple_project()

        self.assertNotEqual(ProjectContainsDevice(project), IsDevice())
