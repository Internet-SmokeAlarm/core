import unittest
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import User
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.controller.utils.user import handle_load_user


class HandleLoadUserTestCase(unittest.TestCase):

    def _create_empty_user(self) -> User:
        return User("valetolpegin", [], [])

    def test_handle_load_user_pass(self):
        db = InMemoryDBInterface()
        correct_user = self._create_empty_user()

        loaded_user = handle_load_user(db, "valetolpegin")

        self.assertEqual(correct_user, loaded_user)
        self.assertEqual(DBObject.load_from_db(User, "valetolpegin", db), correct_user)

    def test_handle_load_user_pass_2(self):
        db = InMemoryDBInterface()
        correct_user = self._create_empty_user()
        correct_user.add_api_key("adf234sdf7gfh678fgh23x")
        correct_user.save_to_db(db)

        loaded_user = handle_load_user(db, "valetolpegin")

        self.assertEqual(correct_user, loaded_user)
