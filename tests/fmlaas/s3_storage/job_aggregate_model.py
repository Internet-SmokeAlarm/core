import unittest
from dependencies.python.fmlaas.s3_storage import JobAggregateModelPointer


class JobAggregateModelPointerTestCase(unittest.TestCase):

    def test_str_pass(self):
        pointer = JobAggregateModelPointer("project_id_123", "experiment_id_123", "job_id_123")
        correct_str_repr = "project_id_123/experiment_id_123/job_id_123/aggregate_model"

        self.assertEqual(str(pointer), correct_str_repr)

    def test_from_str_pass(self):
        correct_pointer_repr = JobAggregateModelPointer("project_id_123", "experiment_id_123", "job_id_123")
        pointer = JobAggregateModelPointer.from_str("project_id_123/experiment_id_123/job_id_123/aggregate_model")

        self.assertEqual(correct_pointer_repr, pointer)
