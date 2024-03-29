import unittest

from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.model import ApiKeyTypeEnum


class AuthContextProcessorTestCase(unittest.TestCase):

    def test_get_auth_type_pass(self):
        data = {
            "authentication_type": "JWT"
        }

        auth_context = AuthContextProcessor(data)

        self.assertEqual(ApiKeyTypeEnum.JWT, auth_context.get_type())
        self.assertTrue(auth_context.is_type_user())
        self.assertFalse(auth_context.is_type_device())

    def test_get_auth_type_fail(self):
        data = {}

        auth_context = AuthContextProcessor(data)

        self.assertRaises(ValueError, auth_context.get_type)

    def test_get_entity_id_pass(self):
        data = {
            "entity_id": "12344"
        }

        auth_context = AuthContextProcessor(data)

        self.assertEqual("12344", auth_context.get_entity_id())

    def test_get_entity_id_fail(self):
        data = {}

        auth_context = AuthContextProcessor(data)

        self.assertRaises(ValueError, auth_context.get_entity_id)
