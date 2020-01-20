import unittest

from dependencies.python.fmlaas.model import ApiKey
from dependencies.python.fmlaas.model import ApiKeyBuilder
from dependencies.python.fmlaas.auth import PermissionsGroupTypeEnum

class ApiKeyTestCase(unittest.TestCase):

    def _build_default_api_key(self):
        builder = ApiKeyBuilder()
        builder.set_permissions_group(PermissionsGroupTypeEnum.GROUP_ADMIN)

        return builder.build()

    def test_to_json_pass(self):
        api_key = self._build_default_api_key()

        key_json = api_key.to_json()

        self.assertEqual({}, key_json["event_log"])
        self.assertIsNotNone(key_json["ID"])
        self.assertIsNotNone(key_json["hash"])
        self.assertIsNotNone(key_json["created_on"])

    def test_from_json_pass(self):
        api_key = self._build_default_api_key()

        key_json = api_key.to_json()

        new_key = ApiKey.from_json(key_json)

        self.assertEqual(new_key.get_event_log(), api_key.get_event_log())
        self.assertEqual(new_key.get_hash(), api_key.get_hash())
        self.assertEqual(new_key.get_id(), api_key.get_id())
        self.assertEqual(new_key.get_created_on(), api_key.get_created_on())
