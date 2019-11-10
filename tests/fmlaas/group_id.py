import unittest

from dependencies.python.fmlaas import generate_unique_id

class GenerateUniqueIdTestCase(unittest.TestCase):

    def test_generate_group_id(self):
        unique_id = generate_unique_id()

        self.assertEqual(len(str(unique_id)), 16)
        self.assertTrue(type(unique_id), type(1))
