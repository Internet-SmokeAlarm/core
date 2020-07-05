import unittest
from dependencies.python.fmlaas.s3_storage import StartModelPointer


class StartModelPointerTestCase(unittest.TestCase):

    def test_str_pass(self):
        pointer = StartModelPointer("project_id_123", "experiment_id_123")
        correct_str_repr = "project_id_123/experiment_id_123/start_model"

        self.assertEqual(str(pointer), correct_str_repr)

    def test_from_str_pass(self):
        correct_pointer_repr = StartModelPointer("project_id_123", "experiment_id_123")
        pointer = StartModelPointer.from_str("project_id_123/experiment_id_123/start_model")

        self.assertEqual(correct_pointer_repr, pointer)
