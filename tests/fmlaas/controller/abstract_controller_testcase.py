from .abstract_testcase import AbstractTestCase
from dependencies.python.fmlaas.controller.utils.auth.conditions import AbstractCondition
from dependencies.python.fmlaas.controller import AbstractController
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.exception import RequestForbiddenException

class DummyAuthVerifier(AbstractCondition):

    def __init__(self, val: bool):
        self.val = val

    def verify(self, auth_context: AuthContextProcessor) -> bool:
        return self.val

class AbstractControllerTestCase(AbstractTestCase):

    def test_verify_auth_fail(self):
        class DummyController(AbstractController):

            def get_auth_conditions(self):
                return [
                    [
                        DummyAuthVerifier(True),
                        DummyAuthVerifier(False),
                        DummyAuthVerifier(True)
                    ],
                    [
                        DummyAuthVerifier(True),
                        DummyAuthVerifier(False)
                    ]
                ]

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = DummyController(auth_context)

        self.assertRaises(RequestForbiddenException, controller.verify_auth)

    def test_verify_auth_pass(self):
        class DummyController(AbstractController):

            def get_auth_conditions(self):
                return [
                    [
                        DummyAuthVerifier(True),
                        DummyAuthVerifier(True),
                        DummyAuthVerifier(True)
                    ],
                    [
                        DummyAuthVerifier(True),
                        DummyAuthVerifier(False)
                    ]
                ]

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "user_123442"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = DummyController(auth_context)

        controller.verify_auth()
