import unittest

from dependencies.python.fmlaas import generate_unique_id

class GenerateUniqueIdTestCase(unittest.TestCase):

    def test_pass(self):
        unique_id = generate_unique_id()

        self.assertEqual(len(str(unique_id)), 32)
        self.assertTrue(type(unique_id), type("1"))
