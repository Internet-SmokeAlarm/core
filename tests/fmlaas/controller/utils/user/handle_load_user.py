import unittest

from dependencies.python.fmlaas.controller.utils.user import handle_load_user
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import User


class HandleLoadUserTestCase(unittest.TestCase):

    def _create_empty_user(self) -> User:
        return User("valetolpegin", {}, set())

    def test_handle_load_user_pass(self):
        db = InMemoryDBInterface()

        loaded_user = handle_load_user(db, "valetolpegin")

        self.assertIsNone(loaded_user)

    def test_handle_load_user_pass_2(self):
        db = InMemoryDBInterface()
        correct_user = self._create_empty_user()
        correct_user.save_to_db(db)

        loaded_user = handle_load_user(db, "valetolpegin")

        self.assertEqual(correct_user, loaded_user)
