import unittest

from dependencies.python.fmlaas.auth import generate_secret

class KeyGenerationTestCase(unittest.TestCase):

    def test_generate_secret(self):
        key = generate_secret()

        self.assertIsNotNone(key)
