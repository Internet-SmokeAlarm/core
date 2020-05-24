import unittest

from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model.termination_criteria import DurationTerminationCriteria


class JobConfigurationTestCase(unittest.TestCase):

    def test_to_json_pass(self):
        job_configuration = JobConfiguration(50, 5, "RANDOM", [
            DurationTerminationCriteria(50, 123211241.2342).to_json()
        ])

        job_configuration_json = job_configuration.to_json()

        self.assertEqual(job_configuration_json["num_devices"], "50")
        self.assertEqual(
            job_configuration_json["device_selection_strategy"],
            "RANDOM")
        self.assertEqual(job_configuration_json["num_buffer_devices"], "5")
        self.assertEqual(
            job_configuration_json["termination_criteria"][0],
            {
                'type': 'DurationTerminationCriteria',
                'max_duration_sec': '50',
                'start_epoch_time': '123211241.2342'})

    def test_from_json_pass(self):
        job_configuration_json = {
            'num_devices': "50",
            'num_buffer_devices': "5",
            "device_selection_strategy": "RANDOM",
            "termination_criteria": [
                {
                    'type': 'DurationTerminationCriteria',
                    'max_duration_sec': '50',
                    'start_epoch_time': '123211241.2342'}]}

        job_configuration = JobConfiguration.from_json(job_configuration_json)

        self.assertEqual(job_configuration.get_num_devices(), 50)
        self.assertEqual(job_configuration.get_num_buffer_devices(), 5)
        self.assertEqual(job_configuration.get_total_num_devices(), 55)
        self.assertEqual(
            job_configuration.get_device_selection_strategy(),
            "RANDOM")
        self.assertEqual(
            job_configuration.get_termination_criteria()[0].to_json(),
            {
                'type': 'DurationTerminationCriteria',
                'max_duration_sec': '50',
                'start_epoch_time': '123211241.2342'})

    def test_add_termination_criteria(self):
        job_configuration = JobConfiguration(50, 0, "RANDOM", [])

        self.assertEqual(len(job_configuration.get_termination_criteria()), 0)

        job_configuration_json = job_configuration.add_termination_criteria(
            DurationTerminationCriteria(50, 123211241.2342))

        self.assertEqual(len(job_configuration.get_termination_criteria()), 1)
        self.assertEqual(
            type(
                job_configuration.get_termination_criteria()[0]),
            DurationTerminationCriteria)

    def test_set_termination_criteria(self):
        job_configuration = JobConfiguration(50, 0, "RANDOM", [])

        self.assertEqual(len(job_configuration.get_termination_criteria()), 0)

        job_configuration_json = job_configuration.set_termination_criteria(
            [DurationTerminationCriteria(50, 123211241.2342)])

        self.assertEqual(len(job_configuration.get_termination_criteria()), 1)
        self.assertEqual(
            type(
                job_configuration.get_termination_criteria()[0]),
            DurationTerminationCriteria)

    def test_get_total_num_devices(self):
        job_configuration = JobConfiguration(50, 5, "RANDOM", [])

        self.assertEqual(job_configuration.get_total_num_devices(), 55)

    def test_reset_termination_criteria_pass(self):
        job_configuration = JobConfiguration(50, 5, "RANDOM", [
            DurationTerminationCriteria(50, 123211241.2342).to_json()
        ])

        job_configuration.reset_termination_criteria()

        self.assertNotEqual(job_configuration.get_termination_criteria()[
                            0].get_start_epoch_time(), 123211241.2342)
