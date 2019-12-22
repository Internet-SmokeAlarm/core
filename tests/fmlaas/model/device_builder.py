import unittest

from dependencies.python.fmlaas.model import DeviceBuilder

class DeviceBuilderTestCase(unittest.TestCase):

    def test_build_pass(self):
        builder = DeviceBuilder()
        builder.set_id("test_id")
        device = builder.build()

        self.assertEqual(device.get_id(), "test_id")

    def test_build_fail_1(self):
        builder = DeviceBuilder()

        self.assertRaises(ValueError, builder.build)

    def test_build_fail_2(self):
        builder = DeviceBuilder()
        builder.set_id(123123123)

        self.assertRaises(ValueError, builder.build)

    def test_validate_parameters_pass(self):
        builder = DeviceBuilder()
        builder.set_id("test_id")

        builder._validate_parameters()

    def test_validate_parameters_fail(self):
        builder = DeviceBuilder()

        self.assertRaises(ValueError, builder._validate_parameters)

    def test_validate_parameters_fail_2(self):
        builder = DeviceBuilder()
        builder.set_id(123123123)

        self.assertRaises(ValueError, builder._validate_parameters)
