import unittest

from dependencies.python.fmlaas.request_processor import JobConfigJSONProcessor
from dependencies.python.fmlaas.model import JobConfiguration


class JobConfigJSONProcessorTestCase(unittest.TestCase):

    def test_get_device_selection_strategy_pass(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": 10,
            "num_buffer_devices": 0,
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        device_selection_strategy = config_processor.get_device_selection_strategy()

        self.assertEqual("RANDOM", device_selection_strategy)

    def test_get_device_selection_strategy_fail(self):
        data = {
            "device_selection_strategy": 120123,
            "num_devices": 10,
            "num_buffer_devices": 0,
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        self.assertRaises(
            ValueError,
            config_processor.get_device_selection_strategy)

    def test_get_device_selection_strategy_fail_2(self):
        data = {
            "device_selection_strategy": None,
            "num_devices": 10,
            "num_buffer_devices": 0,
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        self.assertRaises(
            ValueError,
            config_processor.get_device_selection_strategy)

    def test_get_device_selection_strategy_fail_3(self):
        data = {
            "device_selection_strategy": {},
            "num_devices": 10,
            "num_buffer_devices": 0,
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        self.assertRaises(
            ValueError,
            config_processor.get_device_selection_strategy)

    def test_get_num_devices_pass(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": 10,
            "num_buffer_devices": 0,
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        num_devices = config_processor.get_num_devices()

        self.assertEqual(10, num_devices)

    def test_get_num_devices_fail(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": "10",
            "num_buffer_devices": 0,
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_num_devices)

    def test_get_num_devices_fail_2(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": None,
            "num_buffer_devices": 0,
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_num_devices)

    def test_get_num_devices_fail_3(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": {},
            "num_buffer_devices": 0,
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_num_devices)

    def test_get_num_buffer_devices_pass(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": 0,
            "num_buffer_devices": 4,
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        self.assertEqual(4, config_processor.get_num_buffer_devices())

    def test_get_num_buffer_devices_fail(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": 0,
            "num_buffer_devices": None,
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_num_buffer_devices)

    def test_get_num_buffer_devices_fail_2(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": 0,
            "num_buffer_devices": "1231",
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_num_buffer_devices)

    def test_get_num_buffer_devices_fail_3(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": 0,
            "num_buffer_devices": {},
            "termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_num_buffer_devices)

    def test_get_termination_criteria_pass(self):
        data = {"termination_criteria": []}
        config_processor = JobConfigJSONProcessor(data)

        self.assertEqual([], config_processor.get_termination_criteria())

    def test_get_termination_criteria_fail(self):
        data = {}
        config_processor = JobConfigJSONProcessor(data)

        self.assertRaises(
            ValueError,
            config_processor.get_termination_criteria)

    def test_generate_job_config(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": 10,
            "num_buffer_devices": 0,
            "termination_criteria": []}

        config_processor = JobConfigJSONProcessor(data)
        job_config = config_processor.generate_job_config()

        self.assertEqual(JobConfiguration, job_config.__class__)
        self.assertEqual(10, job_config.get_num_devices())

    def test_generate_job_config_pass_2(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": 10,
            "num_buffer_devices": 5,
            "termination_criteria": [
                {
                    "type": "DurationTerminationCriteria",
                    "max_duration_sec": 50
                }
            ]
        }

        config_processor = JobConfigJSONProcessor(data)
        job_config = config_processor.generate_job_config()

        self.assertEqual(JobConfiguration, job_config.__class__)
        self.assertEqual(10, job_config.get_num_devices())
        self.assertEqual(5, job_config.get_num_buffer_devices())
        self.assertEqual(15, job_config.get_total_num_devices())
        self.assertEqual(len(job_config.get_termination_criteria()), 1)
        self.assertEqual(job_config.get_termination_criteria()
                         [0].get_max_duration_sec(), 50)

    def test_generate_job_config_pass_3(self):
        data = {
            "device_selection_strategy": "RANDOM",
            "num_devices": 10,
            "num_buffer_devices": 0,
            "termination_criteria": [
                {
                    "type": "DurationTerminationCriteria",
                    "max_duration_sec": 50
                },
                {
                    "type": "DurationTerminationCriteria",
                    "max_duration_sec": 100
                }
            ]
        }

        config_processor = JobConfigJSONProcessor(data)
        job_config = config_processor.generate_job_config()

        self.assertEqual(JobConfiguration, job_config.__class__)
        self.assertEqual(10, job_config.get_num_devices())
        self.assertEqual(0, job_config.get_num_buffer_devices())
        self.assertEqual(10, job_config.get_total_num_devices())
        self.assertEqual(len(job_config.get_termination_criteria()), 2)
        self.assertEqual(job_config.get_termination_criteria()
                         [0].get_max_duration_sec(), 50)
        self.assertEqual(job_config.get_termination_criteria()
                         [1].get_max_duration_sec(), 100)

    def test_load_termination_criteria_fail(self):
        config_processor = JobConfigJSONProcessor({})

        self.assertRaises(
            ValueError, config_processor._load_termination_criteria, {
                "type": None})

    def test_load_termination_criteria_fail_2(self):
        config_processor = JobConfigJSONProcessor({})

        self.assertRaises(
            ValueError, config_processor._load_termination_criteria, {
                "type": "not_duration"})

    def test_load_termination_criteria_pass(self):
        config_processor = JobConfigJSONProcessor({})

        data = {
            "type": "DurationTerminationCriteria",
            "max_duration_sec": 50
        }

        self.assertEqual(50, config_processor._load_termination_criteria(
            data).get_max_duration_sec())
