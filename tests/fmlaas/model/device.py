from dependencies.python.fmlaas.model import Device

from .abstract_model_testcase import AbstractModelTestCase


class DeviceTestCase(AbstractModelTestCase):

    def test_to_from_json(self):
        device = self._create_device("100")

        device_json = device.to_json()
        self.assertEqual("100", device_json["ID"])

        from_json_device = Device.from_json(device_json)
        self.assertEqual(device, from_json_device)
