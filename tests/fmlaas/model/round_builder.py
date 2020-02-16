import unittest

from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import RoundStatus
from dependencies.python.fmlaas.model import RoundConfiguration

class RoundBuilderTestCase(unittest.TestCase):

    def test_build_pass(self):
        round_builder = RoundBuilder()
        round_builder.set_id("test_id")
        round_builder.set_parent_group_id("fl_group_123123")

        configuration = RoundConfiguration("50", "RANDOM")
        round_builder.set_configuration(configuration.to_json())
        round_builder.set_start_model(Model("1234", "1234/start_model", "123211").to_json())

        round = round_builder.build()

        self.assertEqual(round.get_configuration().to_json(), configuration.to_json())
        self.assertEqual(round.get_id(), "test_id")
        self.assertEqual(round.get_start_model().get_entity_id(), "1234")
        self.assertEqual(round.get_status(), RoundStatus.IN_PROGRESS)
        self.assertEqual(round.get_models(), {})
        self.assertEqual(round.aggregate_model, {})
        self.assertEqual(round.get_billable_size(), 0)
        self.assertEqual(len(round.get_devices()), 0)
        self.assertEqual(round.get_parent_group_id(), "fl_group_123123")

    def test_build_fail(self):
        round_builder = RoundBuilder()

        configuration = RoundConfiguration("50", "RANDOM")
        round_builder.set_configuration(configuration.to_json())

        self.assertRaises(ValueError, round_builder.build)

    def test_build_fail_2(self):
        round_builder = RoundBuilder()
        round_builder.set_id("test_id")

        self.assertRaises(ValueError, round_builder.build)

    def test_build_fail_3(self):
        round_builder = RoundBuilder()
        round_builder.set_id("test_id")
        configuration = RoundConfiguration("50", "RANDOM")
        round_builder.set_configuration(configuration.to_json())

        self.assertRaises(ValueError, round_builder.build)

    def test_validate_parameters_pass(self):
        round_builder = RoundBuilder()
        round_builder.set_id("test_id")
        round_builder.set_parent_group_id("fl_group_12312313")

        configuration = RoundConfiguration("50", "RANDOM")
        round_builder.set_configuration(configuration.to_json())

        round_builder.set_start_model(Model("1234", "1234/1234", "123211").to_json())

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

    def test_validate_parameters_fail_3(self):
        round_builder = RoundBuilder()
        round_builder.set_id("test_id")
        configuration = RoundConfiguration("50", "RANDOM")
        round_builder.set_configuration(configuration.to_json())

        self.assertRaises(ValueError, round_builder._validate_parameters)
