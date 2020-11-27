import unittest

from dependencies.python.fmlaas.device_selection import (DeviceSelectorFactory,
                                                         RandomDeviceSelector)
from dependencies.python.fmlaas.model.device_selection_strategy import \
    DeviceSelectionStrategy


class DeviceSelectorFactoryTestCase(unittest.TestCase):

    def test_get_device_selector_pass(self):
        factory = DeviceSelectorFactory()
        device_selector = factory.get_device_selector(DeviceSelectionStrategy.RANDOM)

        self.assertEqual(type(device_selector), RandomDeviceSelector)

    def test_get_device_selector_fail(self):
        factory = DeviceSelectorFactory()

        self.assertRaises(
            ValueError,
            factory.get_device_selector,
            "NOT_RELEVANT_THING_HERE")
