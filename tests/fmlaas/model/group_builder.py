import unittest

from dependencies.python.fmlaas.model import GroupBuilder

class GroupBuilderTestCase(unittest.TestCase):

    def test_build_pass_1(self):
        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        group = builder.build()

        self.assertEqual(group.get_name(), "test_name")
        self.assertEqual(group.get_id(), "test_id")
        self.assertEqual(group.get_devices(), {})
        self.assertEqual(group.get_round_info(), {})
        self.assertEqual(group.get_current_round_ids(), [])
        self.assertEqual(group.get_round_paths(), [])
        self.assertEqual(group.get_billing(), {})

    def test_build_fail_1(self):
        builder = GroupBuilder()
        builder.set_id("test_id")

        self.assertRaises(ValueError, builder.build)

    def test_build_fail_2(self):
        builder = GroupBuilder()
        builder.set_name("test_name")

        self.assertRaises(ValueError, builder.build)

    def test_validate_parameters_pass(self):
        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")

        builder._validate_parameters()

    def test_validate_parameters_fail_1(self):
        builder = GroupBuilder()
        builder.set_id("test_id")

        self.assertRaises(ValueError, builder._validate_parameters)

    def test_validate_parameters_fail_2(self):
        builder = GroupBuilder()
        builder.set_name("test_name")

        self.assertRaises(ValueError, builder._validate_parameters)
