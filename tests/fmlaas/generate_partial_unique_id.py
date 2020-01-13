import unittest

from dependencies.python.fmlaas import generate_partial_unique_id

class GeneratePartialUniqueIdTestCase(unittest.TestCase):

    def test_pass(self):
        unique_id = generate_partial_unique_id()

        self.assertEqual(len(str(unique_id)), 16)
        self.assertTrue(type(unique_id), type("1"))
