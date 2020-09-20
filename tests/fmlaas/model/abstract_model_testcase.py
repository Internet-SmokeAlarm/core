import unittest
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ExperimentBuilder
from dependencies.python.fmlaas.model import ProjectBuilder


class AbstractModelTestCase(unittest.TestCase):

    def _build_default_experiment(self):
        experiment = self._build_parameterized_experiment(1)

        experiment_json = {
            "ID" : "123dafasdf34sdfsdf_1",
            "jobs" : [],
            "current_job" : "NONE",
            "start_model" : {},
            "current_model" : {},
            "hyperparameters" : {},
            "is_active" : False
        }

        return experiment, experiment_json

    def _build_parameterized_experiment(self, id):
        builder = ExperimentBuilder()
        builder.id = "123dafasdf34sdfsdf_{}".format(id)

        return builder.build()

    def _build_job(self, id):
        builder = JobBuilder()
        builder.set_id("test_id_{}".format(id))
        builder.set_experiment_id("123dafasdf34sdfsdf")
        builder.set_project_id("fl_group_1232234")
        builder.set_devices(["123", "234"])
        configuration = JobConfiguration(2, 0, "RANDOM", [])
        builder.set_configuration(configuration.to_json())

        return builder.build()

    def _build_simple_project(self, id):
        builder = ProjectBuilder()
        builder.set_id("id_{}".format(id))
        builder.set_name("my_name")
        builder.set_description("my_description")

        return builder.build()

    def _get_simple_project_json(self, id):
        return {
            'name': 'my_name',
            'description': 'my_description',
            'ID': 'id_{}'.format(id),
            'devices': {},
            "experiments": {},
            "members": {},
            "billing": {}}
