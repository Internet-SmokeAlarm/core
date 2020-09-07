import unittest
from dependencies.python.fmlaas.controller.utils.auth.conditions import UserContainsApiKey
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.model import User
from ....abstract_testcase import AbstractTestCase


class UserContainsApiKeyTestCase(AbstractTestCase):

    def test_verify_pass_false(self):
        user = self._create_empty_user()

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertFalse(UserContainsApiKey(user.user, "test_key_id").verify(auth_context))

    def test_verify_pass_true(self):
        user = self._create_empty_user()
        user.user.add_api_key("test_key_id")

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertTrue(UserContainsApiKey(user.user, "test_key_id").verify(auth_context))

    def test_eq_pass(self):
        user = self._create_empty_user()
        user_2 = self._create_empty_user()
        user_2.user.add_api_key("test_key_id")

        self.assertEqual(UserContainsApiKey(user.user, "test_key_id"), UserContainsApiKey(user.user, "test_key_id"))
        self.assertNotEqual(UserContainsApiKey(user.user, "test_key_id"), UserContainsApiKey(user.user, "test_key_id_3"))
        self.assertNotEqual(UserContainsApiKey(user.user, "test_key_id"), UserContainsApiKey(user_2.user, "test_key_id"))
