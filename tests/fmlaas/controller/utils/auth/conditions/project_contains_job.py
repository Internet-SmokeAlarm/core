import unittest

from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsDevice
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsJob
from ....abstract_testcase import AbstractTestCase


class ProjectContainsJobTestCase(AbstractTestCase):

    def test_verify_pass_false(self):
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        project = self._build_simple_project()
        job = self._build_simple_job()

        self.assertFalse(ProjectContainsJob(project, job).verify(auth_context))

    def test_verify_pass_true(self):
        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        project = self._build_simple_project()
        job = self._build_simple_job()
        experiment = self._build_simple_experiment()
        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        self.assertTrue(ProjectContainsJob(project, job).verify(auth_context))

    def test_eq_pass(self):
        project = self._build_simple_project()
        job = self._build_simple_job()

        self.assertTrue(ProjectContainsJob(project, job) == ProjectContainsJob(project, job))

    def test_eq_fail(self):
        project = self._build_simple_project()
        job = self._build_simple_job()
        experiment = self._build_simple_experiment()
        experiment.add_job(job)

        project_2 = self._build_simple_project()
        project_2.add_or_update_experiment(experiment)

        self.assertFalse(ProjectContainsJob(project, job) == ProjectContainsJob(project_2, job))
