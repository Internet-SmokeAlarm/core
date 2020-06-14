import unittest

from dependencies.python.fmlaas.model import ApiKeyTypeEnum
from dependencies.python.fmlaas.request_processor import KeyTypeProcessor


class KeyTypeProcessorTestCase(unittest.TestCase):

    def test_get_permissions_project_pass_1(self):
        json_data = {
            "KEY_TYPE": "USER"
        }

        key_type = KeyTypeProcessor(json_data).get_key_type()

        self.assertEqual(ApiKeyTypeEnum.USER, key_type)

    def test_get_permissions_project_fail(self):
        json_data = {}

        self.assertRaises(ValueError, KeyTypeProcessor(json_data).get_key_type)

    def test_get_permissions_project_fail_2(self):
        json_data = {}

        self.assertRaises(
            ValueError,
            KeyTypeProcessor(json_data).get_key_type,
            throw_exception=False)
