import unittest

from dependencies.python.fmlaas.auth import generate_secret
from dependencies.python.fmlaas.auth import generate_key_pair

class KeyGenerationTestCase(unittest.TestCase):

    def test_generate_secret(self):
        key = generate_secret()

        self.assertIsNotNone(key)

    def test_generate_key_pair(self):
        id, key = generate_key_pair()

        self.assertEqual(36, len(id))
        self.assertTrue(id in key)
