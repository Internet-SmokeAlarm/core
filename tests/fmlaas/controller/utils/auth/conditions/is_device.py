import unittest

from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsDevice
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser


class IsDeviceTestCase(unittest.TestCase):

    def test_verify_pass_false(self):
        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertFalse(IsDevice().verify(auth_context))

    def test_verify_pass_false_2(self):
        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertFalse(IsDevice().verify(auth_context))

    def test_verify_pass_true(self):
        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertTrue(IsDevice().verify(auth_context))

    def test_eq_pass(self):
        self.assertTrue(IsDevice() == IsDevice())

    def test_eq_fail(self):
        self.assertFalse(IsUser() == IsDevice())
