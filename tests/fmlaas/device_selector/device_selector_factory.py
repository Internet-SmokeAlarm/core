import unittest

from dependencies.python.fmlaas.device_selection import DeviceSelectorFactory
from dependencies.python.fmlaas.device_selection import RandomDeviceSelector

class DeviceSelectorFactoryTestCase(unittest.TestCase):

    def test_get_device_selector_pass(self):
        factory = DeviceSelectorFactory()
        device_selector = factory.get_device_selector("RANDOM")

        self.assertEqual(type(device_selector), RandomDeviceSelector)

    def test_get_device_selector_fail(self):
        factory = DeviceSelectorFactory()

        self.assertRaises(ValueError, factory.get_device_selector, "NOT_RELEVANT_THING_HERE")
