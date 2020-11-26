import unittest
from typing import List

from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model.device_selection_strategy import \
    DeviceSelectionStrategy
from dependencies.python.fmlaas.request_processor import JobConfigJSONProcessor


class JobConfigJSONProcessorTestCase(unittest.TestCase):

    def _create_json_processor(self,
                               selection_strategy: str = "RANDOM",
                               num_devices: int = 10,
                               num_backup_devices: int = 0,
                               termination_criteria: List = []) -> JobConfigJSONProcessor:
        json_data = {
            "device_selection_strategy": selection_strategy,
            "num_devices": num_devices,
            "num_backup_devices": num_backup_devices,
            "termination_criteria": termination_criteria}
        config_processor = JobConfigJSONProcessor(json_data) 

        return config_processor, json_data

    def test_get_device_selection_strategy_pass(self):
        config_processor, _ = self._create_json_processor()

        device_selection_strategy = config_processor.get_device_selection_strategy()

        self.assertEqual(DeviceSelectionStrategy.RANDOM, device_selection_strategy)

    def test_get_device_selection_strategy_fail(self):
        config_processor, _ = self._create_json_processor(selection_strategy=1234)

        self.assertRaises(
            ValueError,
            config_processor.get_device_selection_strategy)

    def test_get_num_devices_pass(self):
        config_processor, _ = self._create_json_processor()

        num_devices = config_processor.get_num_devices()

        self.assertEqual(10, num_devices)

    def test_get_num_devices_fail(self):
        config_processor, _ = self._create_json_processor(num_devices="123")

        self.assertRaises(ValueError, config_processor.get_num_devices)

    def test_get_num_backup_devices_pass(self):
        config_processor, _ = self._create_json_processor()

        self.assertEqual(0, config_processor.get_num_backup_devices())

    def test_get_num_backup_devices_fail(self):
        config_processor, _ = self._create_json_processor(num_backup_devices={})

        self.assertRaises(ValueError, config_processor.get_num_backup_devices)

    def test_get_termination_criteria_pass(self):
        config_processor, _ = self._create_json_processor()

        self.assertEqual([], config_processor.get_termination_criteria())

    def test_get_termination_criteria_fail(self):
        config_processor, _ = self._create_json_processor(termination_criteria=None)

        self.assertRaises(ValueError, config_processor.get_termination_criteria)

    def test_generate_job_config(self):
        termination_criteria = [
            {
                "type": "DurationTerminationCriteria",
                "max_duration_sec": 50
            }
        ]
        config_processor, json_data = self._create_json_processor(termination_criteria=termination_criteria)

        job_config = config_processor.generate_job_config()

        self.assertEqual(JobConfiguration, job_config.__class__)
        self.assertEqual(10, job_config.num_devices)
        self.assertTrue(job_config.termination_criteria[0].max_duration_sec, 50)
