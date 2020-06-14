from dependencies.python.fmlaas.model import ExperimentBuilder
from .abstract_model_testcase import AbstractModelTestCase

class ExperimentBuilderTestCase(AbstractModelTestCase):

    def test_build_pass(self):
        builder = ExperimentBuilder()
        builder.id = "experiment_id_1"

        experiment = builder.build()

        self.assertEqual(experiment.id, "experiment_id_1")

    def test_build_fail(self):
        builder = ExperimentBuilder()

        self.assertRaises(ValueError, builder.build)

    def test_validate_parameters_pass(self):
        builder = ExperimentBuilder()
        builder.id = "experiment_id_1"

        builder._validate_parameters()

    def test_validate_parameters_fail_id_not_set(self):
        builder = ExperimentBuilder()

        self.assertRaises(ValueError, builder._validate_parameters)

    def test_validate_parameters_fail_id_invalid_type(self):
        builder = ExperimentBuilder()
        builder.id = {}

        self.assertRaises(ValueError, builder._validate_parameters)
