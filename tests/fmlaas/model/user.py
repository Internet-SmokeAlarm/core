from dependencies.python.fmlaas.model import User

from .abstract_model_testcase import AbstractModelTestCase


class UserTestCase(AbstractModelTestCase):

    def test_add_project_pass(self):
        user, _ = self._create_test_user()
        new_projects = {
            "123123": {
                "id": "123123",
                "name": "vales_third_project"
            }
        }
        user.add_project(new_projects["123123"]["id"], new_projects["123123"]["name"])

        self.assertEqual(user.projects, new_projects)

    def test_add_api_key_pass(self):
        user, _ = self._create_test_user()
        api_key, _ = self._create_api_key()

        user.add_api_key(api_key.id)

        self.assertEqual(user.api_keys, set([api_key.id]))

    def test_to_json_pass(self):
        user, json_repr = self._create_test_user()

        self.assertEqual(user.to_json(), json_repr)

    def test_from_json_pass(self):
        user, json_repr = self._create_test_user()
        
        self.assertEqual(user, User.from_json(json_repr))

    def test_eq_pass(self):
        user_1, _ = self._create_test_user()
        user_2, _ = self._create_test_user()
        user_3, _ = self._create_test_user(username="tolpv")

        self.assertEqual(user_1, user_2)
        self.assertNotEqual(user_3, user_1)

    def test_contains_api_key_pass(self):
        user, _ = self._create_test_user()
        api_key, _ = self._create_api_key()
        api_key_2, _ = self._create_api_key()

        self.assertFalse(user.contains_api_key(api_key_2.id))
        self.assertFalse(user.contains_api_key(api_key.id))

        user.add_api_key(api_key_2.id)

        self.assertTrue(user.contains_api_key(api_key_2.id))
        self.assertFalse(user.contains_api_key(api_key.id))

    def test_remove_api_key_pass(self):
        user, _ = self._create_test_user()
        api_key, _ = self._create_api_key()
        user.add_api_key(api_key.id)

        user.remove_api_key(api_key.id)

        self.assertEqual(len(user.api_keys), 0)
