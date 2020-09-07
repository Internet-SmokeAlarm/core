import unittest
from collections import namedtuple
from dependencies.python.fmlaas.model import User


class UserTestCase(unittest.TestCase):

    def create_test_user(self) -> User:
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

    def test_construction_and_props_pass(self):
        user_tuple = self.create_test_user()

        self.assertEqual(user_tuple.user.projects, user_tuple.projects)
        self.assertEqual(user_tuple.user.api_keys, user_tuple.api_keys)
        self.assertEqual(user_tuple.user.username, user_tuple.username)

    def test_add_project_pass(self):
        user_tuple = self.create_test_user()

        new_project = {
            "id": "123123",
            "name": "vales_third_project"
        }
        user_tuple.user.add_project(new_project["id"], new_project["name"])

        updated_projects = user_tuple.projects
        updated_projects.append(new_project)

        self.assertEqual(user_tuple.user.projects, updated_projects)

    def test_add_api_keys_pass(self):
        user_tuple = self.create_test_user()

        new_api_key = "adfs23sdfsdfasdf234sdfsd234fsdf12"
        user_tuple.user.add_api_key(new_api_key)

        updated_api_keys = user_tuple.api_keys
        updated_api_keys.append(new_api_key)

        self.assertEqual(user_tuple.user.api_keys, updated_api_keys)

    def test_to_json_pass(self):
        user_tuple = self.create_test_user()

        self.assertEqual(user_tuple.user.to_json(), user_tuple.user_json)

    def test_from_json_pass(self):
        user_tuple = self.create_test_user()

        self.assertEqual(user_tuple.user.from_json(user_tuple.user_json), user_tuple.user)

    def test_eq_pass(self):
        user_tuple_1 = self.create_test_user()
        user_tuple_2 = self.create_test_user()

        self.assertEqual(user_tuple_1.user, user_tuple_2.user)

    def test_eq_fail_1(self):
        user_tuple_1 = self.create_test_user()
        user_tuple_2 = self.create_test_user()

        user_tuple_2.user.add_project("123121234235afaszf1234", "vales_second_project")

        self.assertNotEqual(user_tuple_1.user, user_tuple_2.user)

    def test_eq_fail_2(self):
        user_tuple_1 = self.create_test_user()
        user_tuple_2 = self.create_test_user()

        user_tuple_2.user.add_api_key("123121234235afaszf1234")

        self.assertNotEqual(user_tuple_1.user, user_tuple_2.user)

    def test_contains_api_key_pass(self):
        user_tuple = self.create_test_user()

        self.assertTrue(user_tuple.user.contains_api_key(user_tuple.api_keys[0]))
        self.assertTrue(user_tuple.user.contains_api_key(user_tuple.api_keys[1]))
        self.assertTrue(user_tuple.user.contains_api_key(user_tuple.api_keys[2]))
        self.assertFalse(user_tuple.user.contains_api_key("test_api_key"))

    def test_remove_api_key_pass(self):
        user_tuple = self.create_test_user()

        user_tuple.user.remove_api_key(user_tuple.api_keys[0])

        self.assertEqual(len(user_tuple.user.api_keys), 2)
