import unittest

from dependencies.python.fmlaas import generate_device_key_pair

class DeviceKeyTestCase(unittest.TestCase):

    def test_generate_device_key_pair(self):
        device_id, device_api_key = generate_device_key_pair()

        self.assertEqual(len(str(device_id)), 16)
        self.assertEqual(len(device_api_key), 36)

        self.assertEqual(type(device_id), type(0))
        self.assertEqual(type(device_api_key), type("string"))
