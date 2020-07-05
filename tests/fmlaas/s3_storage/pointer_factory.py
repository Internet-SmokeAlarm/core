import unittest
from dependencies.python.fmlaas.s3_storage import JobAggregateModelPointer
from dependencies.python.fmlaas.s3_storage import StartModelPointer
from dependencies.python.fmlaas.s3_storage import DeviceModelPointer
from dependencies.python.fmlaas.s3_storage import PointerFactory
from dependencies.python.fmlaas.s3_storage import PointerType


class PointerFactoryTestCase(unittest.TestCase):

    def test_load_pointer_pass(self):
        job_aggregate_model = JobAggregateModelPointer("project_id_123", "experiment_id_123", "job_id_123")
        start_model = StartModelPointer("project_id_123", "experiment_id_123")
        device_model = DeviceModelPointer("project_id_123", "experiment_id_123", "job_id_123", "device_id_123")

        self.assertEqual(job_aggregate_model, PointerFactory.load_pointer(str(job_aggregate_model)))
        self.assertEqual(start_model, PointerFactory.load_pointer(str(start_model)))
        self.assertEqual(device_model, PointerFactory.load_pointer(str(device_model)))

    def test_get_pointer_type_pass(self):
        job_aggregate_model = "project_id_123/experiment_id_123/job_id_123/job_aggregate_model"
        start_model = "project_id_123/experiment_id_123/start_model"
        device_model = "project_id_123/experiment_id_123/job_id_123/device_models/device_id_123"

        self.assertEqual(PointerType.DEVICE_MODEL_UPDATE, PointerFactory.get_pointer_type(device_model))
        self.assertEqual(PointerType.JOB_AGGREGATE_MODEL, PointerFactory.get_pointer_type(job_aggregate_model))
        self.assertEqual(PointerType.EXPERIMENT_START_MODEL, PointerFactory.get_pointer_type(start_model))
