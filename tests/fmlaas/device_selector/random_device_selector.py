import unittest

from dependencies.python.fmlaas.device_selection import RandomDeviceSelector
from dependencies.python.fmlaas.model import JobConfiguration

class RandomDeviceSelectorTestCase(unittest.TestCase):

    def test_select_devices_pass(self):
        selector = RandomDeviceSelector()

        configuration = JobConfiguration(3, 1, "RANDOM", [])

        devices_to_pick = ["123", "456", "789", "101"]

        randomly_selected_devices = selector.select_devices(devices_to_pick, configuration)

        self.assertEqual(4, len(randomly_selected_devices))
        self.assertTrue(randomly_selected_devices[0] in devices_to_pick)
        self.assertTrue(randomly_selected_devices[1] in devices_to_pick)
        self.assertTrue(randomly_selected_devices[2] in devices_to_pick)
        self.assertTrue(randomly_selected_devices[3] in devices_to_pick)

    def test_select_devices_fail_too_many_devices(self):
        selector = RandomDeviceSelector()

        configuration = JobConfiguration(10, 0, "RANDOM", [])

        devices_to_pick = ["123", "456", "789", "101"]

        self.assertRaises(ValueError, selector.select_devices, devices_to_pick, configuration)

    def test_select_devices_fail_too_many_devices(self):
        selector = RandomDeviceSelector()

        configuration = JobConfiguration(1, 6, "RANDOM", [])

        devices_to_pick = ["123", "456", "789", "101"]

        self.assertRaises(ValueError, selector.select_devices, devices_to_pick, configuration)
