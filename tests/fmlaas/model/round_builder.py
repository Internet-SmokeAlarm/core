import unittest

from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import RoundStatus
from dependencies.python.fmlaas.model import RoundConfiguration

class RoundBuilderTestCase(unittest.TestCase):

    def test_build_pass(self):
        round_builder = RoundBuilder()
        round_builder.set_id("test_id")

        configuration = RoundConfiguration("50", "RANDOM")
        round_builder.set_configuration(configuration.to_json())

        round = round_builder.build()

        self.assertEqual(round.get_configuration(), configuration.to_json())
        self.assertEqual(round.get_id(), "test_id")
        self.assertEqual(round.get_previous_round_id(), "N/A")
        self.assertEqual(round.get_status(), RoundStatus.IN_PROGRESS)
        self.assertEqual(round.get_models(), {})
        self.assertEqual(len(round.get_devices()), 0)

    def test_build_fail(self):
        round_builder = RoundBuilder()

        configuration = RoundConfiguration("50", "RANDOM")
        round_builder.set_configuration(configuration.to_json())

        self.assertRaises(ValueError, round_builder.build)

    def test_build_fail_2(self):
        round_builder = RoundBuilder()
        round_builder.set_id("test_id")

        self.assertRaises(ValueError, round_builder.build)

    def test_validate_parameters_pass(self):
        round_builder = RoundBuilder()
        round_builder.set_id("test_id")

        configuration = RoundConfiguration("50", "RANDOM")
        round_builder.set_configuration(configuration.to_json())

        round_builder._validate_parameters()

    def test_validate_parameters_fail(self):
        round_builder = RoundBuilder()

        configuration = RoundConfiguration("50", "RANDOM")
        round_builder.set_configuration(configuration.to_json())

        self.assertRaises(ValueError, round_builder._validate_parameters)

    def test_validate_parameters_fail_2(self):
        round_builder = RoundBuilder()
        round_builder.set_id("test_id")

        self.assertRaises(ValueError, round_builder._validate_parameters)
