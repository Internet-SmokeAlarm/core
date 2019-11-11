import unittest

from dependencies.python.fmlaas import generate_model_object_name

class GenerateModelObjectNameTestCase(unittest.TestCase):

    def test_generate_model_object_name(self):
        name = generate_model_object_name(12, 1000)

        self.assertEqual("12_1000", name)
