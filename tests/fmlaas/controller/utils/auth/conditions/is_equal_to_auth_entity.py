import unittest

from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    IsEqualToAuthEntity, IsUser)
from dependencies.python.fmlaas.request_processor import AuthContextProcessor


class IsEqualToAuthEntityTestCase(unittest.TestCase):

    def test_verify_pass_false(self):
        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertFalse(IsEqualToAuthEntity("user_12344").verify(auth_context))

    def test_verify_pass_true(self):
        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertTrue(IsEqualToAuthEntity("user_123442").verify(auth_context))

    def test_eq_pass(self):
        self.assertTrue(IsEqualToAuthEntity("woot") == IsEqualToAuthEntity("woot"))

    def test_eq_fail(self):
        self.assertFalse(IsEqualToAuthEntity("woot") == IsUser())
