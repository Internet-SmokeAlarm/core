import unittest

from dependencies.python.fmlaas.request_processor import RoundConfigJSONProcessor
from dependencies.python.fmlaas.model import RoundConfiguration

class RoundConfigJSONProcessorTestCase(unittest.TestCase):

    def test_get_device_selection_strategy_pass(self):
        data = {"device_selection_strategy" : "RANDOM", "num_devices" : 10, "termination_criteria" : []}
        config_processor = RoundConfigJSONProcessor(data)

        device_selection_strategy = config_processor.get_device_selection_strategy()

        self.assertEqual("RANDOM", device_selection_strategy)

    def test_get_device_selection_strategy_fail(self):
        data = {"device_selection_strategy" : 120123, "num_devices" : 10, "termination_criteria" : []}
        config_processor = RoundConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_device_selection_strategy)

    def test_get_device_selection_strategy_fail_2(self):
        data = {"device_selection_strategy" : None, "num_devices" : 10, "termination_criteria" : []}
        config_processor = RoundConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_device_selection_strategy)

    def test_get_device_selection_strategy_fail_3(self):
        data = {"device_selection_strategy" : {}, "num_devices" : 10, "termination_criteria" : []}
        config_processor = RoundConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_device_selection_strategy)

    def test_get_num_devices_pass(self):
        data = {"device_selection_strategy" : "RANDOM", "num_devices" : 10, "termination_criteria" : []}
        config_processor = RoundConfigJSONProcessor(data)

        num_devices = config_processor.get_num_devices()

        self.assertEqual(10, num_devices)

    def test_get_num_devices_fail(self):
        data = {"device_selection_strategy" : "RANDOM", "num_devices" : "10", "termination_criteria" : []}
        config_processor = RoundConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_num_devices)

    def test_get_num_devices_fail_2(self):
        data = {"device_selection_strategy" : "RANDOM", "num_devices" : None, "termination_criteria" : []}
        config_processor = RoundConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_num_devices)

    def test_get_num_devices_fail_3(self):
        data = {"device_selection_strategy" : "RANDOM", "num_devices" : {}, "termination_criteria" : []}
        config_processor = RoundConfigJSONProcessor(data)

        self.assertRaises(ValueError, config_processor.get_num_devices)

    def test_generate_round_config(self):
        data = {"device_selection_strategy" : "RANDOM", "num_devices": 10, "termination_criteria" : []}

        config_processor = RoundConfigJSONProcessor(data)
        round_config = config_processor.generate_round_config()

        self.assertEqual(RoundConfiguration, round_config.__class__)
        self.assertEqual(10, round_config.get_num_devices())
