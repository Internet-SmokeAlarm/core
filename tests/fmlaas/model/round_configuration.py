import unittest

from dependencies.python.fmlaas.model import RoundConfiguration

class RoundConfigurationTestCase(unittest.TestCase):

    def test_to_json_pass(self):
        round_configuration = RoundConfiguration("50")

        round_configuration_json = round_configuration.to_json()

        self.assertEqual(round_configuration_json["num_devices"], "50")

    def test_from_json_pass(self):
        round_configuration_json = {'num_devices': "50"}

        round_configuration = RoundConfiguration.from_json(round_configuration_json)

        self.assertEqual(round_configuration.get_num_devices(), "50")
