import unittest

from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsJobSequence
from ....abstract_testcase import AbstractTestCase


class ProjectContainsJobSequenceTestCase(AbstractTestCase):

    def test_verify_pass_false(self):
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        project = self._build_simple_project()
        job_sequence = self._build_simple_job_sequence()

        self.assertFalse(ProjectContainsJobSequence(project, job_sequence.id).verify(auth_context))

    def test_verify_pass_true(self):
        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        project = self._build_simple_project()
        job_sequence = self._build_simple_job_sequence()
        project.add_or_update_job_sequence(job_sequence)

        self.assertTrue(ProjectContainsJobSequence(project, job_sequence.id).verify(auth_context))

    def test_eq_pass(self):
        project = self._build_simple_project()
        job = self._build_simple_job()

        self.assertTrue(ProjectContainsJobSequence(project, job) == ProjectContainsJobSequence(project, job))

    def test_eq_fail(self):
        project = self._build_simple_project()

        job_sequence = self._build_simple_job_sequence()
        project_2 = self._build_simple_project()
        project_2.add_or_update_job_sequence(job_sequence)

        self.assertFalse(ProjectContainsJobSequence(project, job_sequence.id) == ProjectContainsJobSequence(project_2, job_sequence.id))
