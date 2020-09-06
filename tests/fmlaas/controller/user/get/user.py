import unittest
from typing import List
from typing import Dict
from collections import namedtuple
from dependencies.python.fmlaas.model import User
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.user.get import GetUserController


class GetUserControllerTestCase(unittest.TestCase):

    def _create_prefilled_user(self):
        username = "valetolpegin"
        projects = [
            {
                "id": "123123afsd1234saf23",
                "name": "vales_first_project"
            }
        ]
        api_keys = [
            "12312124afasdf24qfawqr",
            "46435dsfd4234dfgdfg4fg324dfsdf",
            "6y54ewfdsgsy54y0s0ddfsjd"
        ]

        return self._create_user_tuple(username,
                                       projects,
                                       api_keys)

    def _create_empty_user(self):
        username = "valetolpegin"
        projects = []
        api_keys = []

        return self._create_user_tuple(username,
                                       projects,
                                       api_keys)

    def _create_user_tuple(self,
                           username: str,
                           projects: List[Dict[str, str]],
                           api_keys: List[str]):
        user = User(username,
                    projects,
                    api_keys)

        user_json = {
            "ID": username,
            "projects": projects,
            "api_keys": api_keys
        }

        UserTuple = namedtuple("UserTuple", "username projects api_keys user user_json")

        return UserTuple(username,
                         projects,
                         api_keys,
                         user,
                         user_json)

    def test_load_data_pass_1(self):
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
        controller.load_data()

        self.assertEqual(controller._user, user.user)

    def test_load_data_pass_2(self):
        user_db = InMemoryDBInterface()
        user = self._create_empty_user()

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "valetolpegin"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = GetUserController(user_db,
                                           auth_context)
        controller.load_data()

        self.assertEqual(controller._user, user.user)

    def test_get_auth_conditions_pass(self):
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
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser()
            ]
        ]

        self.assertEqual(auth_conditions, correct_auth_conditions)

    def test_execute_pass(self):
        user_db = InMemoryDBInterface()
        user = self._create_prefilled_user()

        user.user.save_to_db(user_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "valetolpegin"
        }
        auth_context = AuthContextProcessor(auth_json)
        loaded_user = GetUserController(user_db,
                                        auth_context).execute()

        self.assertEqual(loaded_user, user.user)
