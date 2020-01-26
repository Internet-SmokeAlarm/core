import unittest

from dependencies.python.fedlearn_auth import generate_key_pair
from dependencies.python.fedlearn_auth import hash_secret
from dependencies.python.fmlaas.model import ApiKeyBuilder

class ApiKeyBuilderTestCase(unittest.TestCase):

    def test_build_pass(self):
        id, key_plaintext = generate_key_pair()
        key_hash = hash_secret(key_plaintext)
        builder = ApiKeyBuilder(id, key_hash)
        builder.set_entity_id("123123")
        builder.set_key_type("USER")
        api_key = builder.build()

        self.assertEqual(api_key.get_entity_id(), "123123")
        self.assertEqual(api_key.get_key_type(), "USER")

    def test_validate_parameters_pass(self):
        id, key_plaintext = generate_key_pair()
        key_hash = hash_secret(key_plaintext)
        builder = ApiKeyBuilder(id, key_hash)
        builder.set_entity_id("123123")
        builder.set_key_type("USER")

        builder._validate_paramaters()

    def test_validate_parameters_fail_1(self):
        id, key_plaintext = generate_key_pair()
        key_hash = hash_secret(key_plaintext)
        builder = ApiKeyBuilder(id, key_hash)
        builder.set_entity_id("123123")

        self.assertRaises(ValueError, builder._validate_paramaters)

    def test_validate_parameters_fail_2(self):
        id, key_plaintext = generate_key_pair()
        key_hash = hash_secret(key_plaintext)
        builder = ApiKeyBuilder(id, key_hash)
        builder.set_key_type("USER")

        self.assertRaises(ValueError, builder._validate_paramaters)
