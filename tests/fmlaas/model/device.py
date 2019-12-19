import unittest

from dependencies.python.fmlaas.model import Device

class DeviceTestCase(unittest.TestCase):

    def test_to_json(self):
        device = Device("my_id", "December 19th, 2019")

        device_json = device.to_json()

        self.assertEqual("my_id", device_json["ID"])
        self.assertEqual("December 19th, 2019", device_json["registered_on"])

    def test_from_json(self):
        device_json = {'ID': 'my_id', 'registered_on': 'December 19th, 2019'}

        device = Device.from_json(device_json)

        self.assertEqual("my_id", device.get_id())
        self.assertEqual("December 19th, 2019", device.get_registered_on())
