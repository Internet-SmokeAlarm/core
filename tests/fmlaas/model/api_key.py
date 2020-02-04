import unittest

from dependencies.python.fedlearn_auth import generate_key_pair
from dependencies.python.fedlearn_auth import hash_secret
from dependencies.python.fmlaas.model import ApiKey
from dependencies.python.fmlaas.model import ApiKeyBuilder

class ApiKeyTestCase(unittest.TestCase):

    def _build_default_api_key(self):
        id, key_plaintext = generate_key_pair()
        key_hash = hash_secret(key_plaintext)
        builder = ApiKeyBuilder(id, key_hash)
        builder.set_entity_id("123123")
        builder.set_key_type("USER")

        return builder.build()

    def test_to_json_pass(self):
        api_key = self._build_default_api_key()

        key_json = api_key.to_json()

        self.assertEqual({}, key_json["event_log"])
        self.assertIsNotNone(key_json["ID"])
        self.assertIsNotNone(key_json["hash"])
        self.assertIsNotNone(key_json["created_on"])
        self.assertEqual(key_json["entity_id"], "123123")
        self.assertEqual(key_json["key_type"], "USER")

    def test_from_json_pass(self):
        api_key = self._build_default_api_key()

        key_json = api_key.to_json()

        new_key = ApiKey.from_json(key_json)

        self.assertEqual(new_key.get_event_log(), api_key.get_event_log())
        self.assertEqual(new_key.get_hash(), api_key.get_hash())
        self.assertEqual(new_key.get_id(), api_key.get_id())
        self.assertEqual(new_key.get_created_on(), api_key.get_created_on())
        self.assertEqual(new_key.get_key_type(), api_key.get_key_type())
        self.assertEqual(new_key.get_entity_id(), api_key.get_entity_id())
