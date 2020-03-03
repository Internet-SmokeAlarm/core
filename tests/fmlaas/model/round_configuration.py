import unittest

from dependencies.python.fmlaas.model import RoundConfiguration
from dependencies.python.fmlaas.model.termination_criteria import DurationTerminationCriteria

class RoundConfigurationTestCase(unittest.TestCase):

    def test_to_json_pass(self):
        round_configuration = RoundConfiguration(50, "RANDOM", [
            DurationTerminationCriteria(50, 123211241.2342).to_json()
        ])

        round_configuration_json = round_configuration.to_json()

        self.assertEqual(round_configuration_json["num_devices"], "50")
        self.assertEqual(round_configuration_json["device_selection_strategy"], "RANDOM")
        self.assertEqual(round_configuration_json["termination_criteria"][0], {'class_name': 'DurationTerminationCriteria', 'max_duration_sec': '50', 'start_epoch_time': '123211241.2342'})

    def test_from_json_pass(self):
        round_configuration_json = {'num_devices': "50", "device_selection_strategy" : "RANDOM", "termination_criteria" : [{'class_name': 'DurationTerminationCriteria', 'max_duration_sec': '50', 'start_epoch_time': '123211241.2342'}]}

        round_configuration = RoundConfiguration.from_json(round_configuration_json)

        self.assertEqual(round_configuration.get_num_devices(), 50)
        self.assertEqual(round_configuration.get_device_selection_strategy(), "RANDOM")
        self.assertEqual(round_configuration.get_termination_criteria()[0].to_json(), {'class_name': 'DurationTerminationCriteria', 'max_duration_sec': '50', 'start_epoch_time': '123211241.2342'})

    def test_add_termination_criteria(self):
        round_configuration = RoundConfiguration(50, "RANDOM", [])

        self.assertEqual(len(round_configuration.get_termination_criteria()), 0)

        round_configuration_json = round_configuration.add_termination_criteria(DurationTerminationCriteria(50, 123211241.2342))

        self.assertEqual(len(round_configuration.get_termination_criteria()), 1)
        self.assertEqual(type(round_configuration.get_termination_criteria()[0]), DurationTerminationCriteria)

    def test_set_termination_criteria(self):
        round_configuration = RoundConfiguration(50, "RANDOM", [])

        self.assertEqual(len(round_configuration.get_termination_criteria()), 0)

        round_configuration_json = round_configuration.set_termination_criteria([DurationTerminationCriteria(50, 123211241.2342)])

        self.assertEqual(len(round_configuration.get_termination_criteria()), 1)
        self.assertEqual(type(round_configuration.get_termination_criteria()[0]), DurationTerminationCriteria)
