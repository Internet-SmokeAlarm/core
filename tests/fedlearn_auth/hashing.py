import unittest

from dependencies.python.fedlearn_auth import hash_secret
from dependencies.python.fedlearn_auth import verify_key
from dependencies.python.fedlearn_auth import generate_key_pair


class HashingTestCase(unittest.TestCase):

    def test_hash_secret_pass(self):
        id, key = generate_key_pair()

        hashed_key = hash_secret(key)

        self.assertIsNotNone(hashed_key)

    def test_verify_key_pass(self):
        id, key = generate_key_pair()

        hash = hash_secret(key)

        self.assertTrue(verify_key(key, hash))
        self.assertFalse(verify_key(id, hash))
        self.assertFalse(verify_key("woo hoo", hash))
