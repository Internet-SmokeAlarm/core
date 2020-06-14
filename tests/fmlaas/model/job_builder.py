import unittest

from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobStatus
from dependencies.python.fmlaas.model import JobConfiguration


class JobBuilderTestCase(unittest.TestCase):

    def test_build_pass(self):
        job_builder = JobBuilder()
        job_builder.set_id("test_id")
        job_builder.set_project_id("fl_project_123123")

        configuration = JobConfiguration(50, 0, "RANDOM", [])
        job_builder.set_configuration(configuration.to_json())
        job_builder.set_start_model(
            Model(
                "1234",
                "1234/start_model",
                "123211").to_json())
        job_builder.set_job_sequence_id("sequence_id_1")

        job = job_builder.build()

        self.assertEqual(
            job.get_configuration().to_json(),
            configuration.to_json())
        self.assertEqual(job.get_id(), "test_id")
        self.assertEqual(job.get_start_model().get_entity_id(), "1234")
        self.assertEqual(job.get_status(), JobStatus.IN_PROGRESS)
        self.assertEqual(job.get_models(), {})
        self.assertEqual(job.aggregate_model, {})
        self.assertEqual(job.get_billable_size(), 0)
        self.assertEqual(len(job.get_devices()), 0)
        self.assertEqual(job.get_project_id(), "fl_project_123123")
        self.assertEqual(job.get_job_sequence_id(), "sequence_id_1")

    def test_build_fail(self):
        job_builder = JobBuilder()

        configuration = JobConfiguration(50, 0, "RANDOM", [])
        job_builder.set_configuration(configuration.to_json())

        self.assertRaises(ValueError, job_builder.build)

    def test_build_fail_2(self):
        job_builder = JobBuilder()
        job_builder.set_id("test_id")

        self.assertRaises(ValueError, job_builder.build)

    def test_build_fail_3(self):
        job_builder = JobBuilder()
        job_builder.set_id("test_id")
        configuration = JobConfiguration(50, 0, "RANDOM", [])
        job_builder.set_configuration(configuration.to_json())

        self.assertRaises(ValueError, job_builder.build)

    def test_validate_parameters_pass(self):
        job_builder = JobBuilder()
        job_builder.set_id("test_id")
        job_builder.set_project_id("fl_project_12312313")
        job_builder.set_job_sequence_id("sequence_id_1")

        configuration = JobConfiguration(50, 0, "RANDOM", [])
        job_builder.set_configuration(configuration.to_json())

        job_builder.set_start_model(
            Model(
                "1234",
                "1234/1234",
                "123211").to_json())

        job_builder._validate_parameters()

    def test_validate_parameters_fail(self):
        job_builder = JobBuilder()

        configuration = JobConfiguration(50, 0, "RANDOM", [])
        job_builder.set_configuration(configuration.to_json())

        self.assertRaises(ValueError, job_builder._validate_parameters)

    def test_validate_parameters_fail_2(self):
        job_builder = JobBuilder()
        job_builder.set_id("test_id")

        self.assertRaises(ValueError, job_builder._validate_parameters)

    def test_validate_parameters_fail_3(self):
        job_builder = JobBuilder()
        job_builder.set_id("test_id")
        configuration = JobConfiguration(50, 0, "RANDOM", [])
        job_builder.set_configuration(configuration.to_json())

        self.assertRaises(ValueError, job_builder._validate_parameters)

    def test_validate_parameters_fail_4(self):
        job_builder = JobBuilder()
        job_builder.set_id("test_id")
        job_builder.set_project_id("fl_project_12312313")

        configuration = JobConfiguration(50, 0, "RANDOM", [])
        job_builder.set_configuration(configuration.to_json())

        job_builder.set_start_model(
            Model(
                "1234",
                "1234/1234",
                "123211").to_json())

        self.assertRaises(ValueError, job_builder._validate_parameters)
