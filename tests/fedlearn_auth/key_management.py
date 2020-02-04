import unittest

from dependencies.python.fedlearn_auth import generate_secret
from dependencies.python.fedlearn_auth import generate_key_pair
from dependencies.python.fedlearn_auth import get_id_from_token

class KeyManagementTestCase(unittest.TestCase):

    def test_generate_secret_pass(self):
        key = generate_secret()

        self.assertIsNotNone(key)

    def test_generate_key_pair_pass(self):
        id, key = generate_key_pair()

        self.assertEqual(32, len(id))
        self.assertTrue(id in key)

    def test_get_id_from_token_pass(self):
        id, key = generate_key_pair()

        self.assertEqual(id, get_id_from_token(key))
