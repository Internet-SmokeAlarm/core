import unittest
from dependencies.python.fmlaas.s3_storage import DeviceModelPointer


class DeviceModelPointerTestCase(unittest.TestCase):

    def test_str_pass(self):
        pointer = DeviceModelPointer("project_id_123", "experiment_id_123", "job_id_123", "device_id_123")
        correct_str_repr = "project_id_123/experiment_id_123/job_id_123/device_models/device_id_123"

        self.assertEqual(str(pointer), correct_str_repr)

    def test_from_str_pass(self):
        correct_pointer_repr = DeviceModelPointer("project_id_123", "experiment_id_123", "job_id_123", "device_id_123")
        pointer = DeviceModelPointer.from_str("project_id_123/experiment_id_123/job_id_123/device_models/device_id_123")

        self.assertEqual(correct_pointer_repr, pointer)
