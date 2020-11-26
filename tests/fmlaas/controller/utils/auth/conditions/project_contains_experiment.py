from dependencies.python.fmlaas.controller.utils.auth.conditions import \
    ProjectContainsExperiment
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ....abstract_testcase import AbstractTestCase


class ProjectContainsExperimentTestCase(AbstractTestCase):

    def test_verify_pass_false(self):
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        project = self._build_simple_project()
        experiment, _ = self._build_simple_experiment("1")

        self.assertFalse(ProjectContainsExperiment(project, experiment.id).verify(auth_context))

    def test_verify_pass_true(self):
        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        project = self._build_simple_project()
        experiment, _ = self._build_simple_experiment("1")
        project.add_or_update_experiment(experiment)

        self.assertTrue(ProjectContainsExperiment(project, experiment.id).verify(auth_context))

    def test_eq_pass(self):
        project = self._build_simple_project()
        experiment, _ = self._build_simple_experiment("1")

        self.assertTrue(ProjectContainsExperiment(project, experiment) == ProjectContainsExperiment(project, experiment))

    def test_eq_fail(self):
        project = self._build_simple_project()

        experiment, _ = self._build_simple_experiment("1")
        project_2 = self._build_simple_project()
        project_2.add_or_update_experiment(experiment)

        self.assertFalse(ProjectContainsExperiment(project, experiment.id) == ProjectContainsExperiment(project_2, experiment.id))
