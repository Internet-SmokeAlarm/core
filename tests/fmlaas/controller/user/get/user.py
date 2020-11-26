from dependencies.python.fmlaas.controller.user.get import GetUserController
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ...abstract_testcase import AbstractTestCase


class GetUserControllerTestCase(AbstractTestCase):

    def test_pass(self):
        user_db = InMemoryDBInterface()
        user = self._create_prefilled_user()

        user.user.save_to_db(user_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "valetolpegin"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = GetUserController(user_db,
                                       auth_context)

        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser()
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)

        # Execute
        loaded_user = controller.execute()
        self.assertEqual(loaded_user, user.user)
