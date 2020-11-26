import unittest

from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import DeviceSelectionStrategy
from dependencies.python.fmlaas.model.termination_criteria import \
    DurationTerminationCriteria


class JobConfigurationTestCase(unittest.TestCase):

    def _create_job_config(self):
        job_config = JobConfiguration(50, 5, DeviceSelectionStrategy.RANDOM, [
            DurationTerminationCriteria(50, 123211241)
        ])

        json_repr = {
            "num_devices": "50",
            "num_backup_devices": "5",
            "device_selection_strategy": "RANDOM",
            "termination_criteria": [
                {
                    "type": DurationTerminationCriteria.__name__,
                    "max_duration_sec": "50",
                    "start_epoch_time": "123211241"
                }
            ]
        }

        return job_config, json_repr

    def test_to_json_pass(self):
        job_config, json_repr = self._create_job_config()

        self.assertEqual(job_config.to_json(), json_repr)

    def test_from_json_pass(self):
        correct_job_config, json_repr = self._create_job_config()

        job_configuration = JobConfiguration.from_json(json_repr)

        self.assertEqual(job_configuration, correct_job_config)

    def test_add_termination_criteria(self):
        job_configuration = JobConfiguration(50, 0, DeviceSelectionStrategy.RANDOM, list())

        self.assertEqual(len(job_configuration.termination_criteria), 0)

        job_configuration.add_termination_criteria(DurationTerminationCriteria(50, 123211241))

        self.assertEqual(len(job_configuration.termination_criteria), 1)
        self.assertEqual(
            type(
                job_configuration.termination_criteria[0]),
            DurationTerminationCriteria)

    def test_set_termination_criteria(self):
        job_configuration = JobConfiguration(50, 0, DeviceSelectionStrategy.RANDOM, list())

        self.assertEqual(len(job_configuration.termination_criteria), 0)

        job_configuration.termination_criteria = [DurationTerminationCriteria(50, 123211241)]

        self.assertEqual(len(job_configuration.termination_criteria), 1)
        self.assertEqual(
            type(
                job_configuration.termination_criteria[0]),
            DurationTerminationCriteria)

    def test_get_total_num_devices(self):
        job_configuration = JobConfiguration(50, 5, DeviceSelectionStrategy.RANDOM, list())

        self.assertEqual(job_configuration.get_total_num_devices(), 55)

    def test_reset_termination_criteria_pass(self):
        job_configuration = JobConfiguration(50, 5, DeviceSelectionStrategy.RANDOM, [
            DurationTerminationCriteria(50, 123211241)
        ])

        job_configuration.reset_termination_criteria()

        self.assertNotEqual(job_configuration.termination_criteria[0].start_epoch_time, 123211241)

    def test_equals_pass_1(self):
        config_1 = JobConfiguration(50, 5, DeviceSelectionStrategy.RANDOM, list())
        config_2 = JobConfiguration(50, 10, DeviceSelectionStrategy.RANDOM, list())

        self.assertFalse(config_1 == config_2)

    def test_equals_pass_2(self):
        config_1 = JobConfiguration(50, 5, DeviceSelectionStrategy.RANDOM, list())
        config_3 = JobConfiguration(50, 5, DeviceSelectionStrategy.RANDOM, list())

        self.assertTrue(config_1 == config_3)

    def test_equals_pass_3(self):
        config_3 = JobConfiguration(50, 5, DeviceSelectionStrategy.RANDOM, list())
        config_4 = JobConfiguration(50, 5, DeviceSelectionStrategy.RANDOM, [DurationTerminationCriteria(50, 123211241)])

        self.assertFalse(config_3 == config_4)

    def test_equals_pass_4(self):
        config_3 = JobConfiguration(50, 5, DeviceSelectionStrategy.RANDOM, [DurationTerminationCriteria(50, 123211241)])
        config_4 = JobConfiguration(50, 5, DeviceSelectionStrategy.RANDOM, [DurationTerminationCriteria(50, 123211241)])

        self.assertTrue(config_3 == config_4)
