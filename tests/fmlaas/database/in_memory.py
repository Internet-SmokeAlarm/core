import unittest
from dependencies.python.fmlaas.database import InMemoryDBInterface


class InMemoryDBInterfaceTestCase(unittest.TestCase):

    def test_create_or_update_object(self):
        db_ = InMemoryDBInterface()

        id = "test_id"
        obj = {"test_key": 10001, "test_key2": "test_value1"}

        db_.create_or_update_object(id, obj)

        self.assertTrue(id in db_.data)
        self.assertEqual(obj, db_.data[id])

    def test_get_object(self):
        db_ = InMemoryDBInterface()

        id = "test_id"
        obj = {"test_key": 10001, "test_key2": "test_value1"}

        db_.create_or_update_object(id, obj)

        resp = db_.get_object(id)

        self.assertEqual(resp, obj)

    def test_delete_object_fail(self):
        db_ = InMemoryDBInterface()

        self.assertRaises(ValueError, db_.delete_object, "test_id")

    def test_get_object_fail(self):
        db_ = InMemoryDBInterface()

        self.assertRaises(ValueError, db_.get_object, "test_id")
