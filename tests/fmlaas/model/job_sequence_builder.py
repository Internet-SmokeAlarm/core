from dependencies.python.fmlaas.model import JobSequenceBuilder
from .abstract_model_testcase import AbstractModelTestCase

class JobSequenceBuilderTestCase(AbstractModelTestCase):

    def test_build_pass(self):
        builder = JobSequenceBuilder()
        builder.id = "sequence_id_1"

        sequence = builder.build()

        self.assertEqual(sequence.id, "sequence_id_1")

    def test_build_fail(self):
        builder = JobSequenceBuilder()

        self.assertRaises(ValueError, builder.build)

    def test_validate_parameters_pass(self):
        builder = JobSequenceBuilder()
        builder.id = "sequence_id_1"

        builder._validate_parameters()

    def test_validate_parameters_fail_id_not_set(self):
        builder = JobSequenceBuilder()

        self.assertRaises(ValueError, builder._validate_parameters)

    def test_validate_parameters_fail_id_invalid_type(self):
        builder = JobSequenceBuilder()
        builder.id = {}

        self.assertRaises(ValueError, builder._validate_parameters)
