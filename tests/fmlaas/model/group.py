import unittest

from dependencies.python.fmlaas import FLGroup
from dependencies.python.fmlaas import generate_device_key_pair
from dependencies.python.fmlaas import InMemoryDBInterface

class FLGroupTestCase(unittest.TestCase):

    def test_add_device(self):
        group = FLGroup("my_name")

        device_id, device_api_key = generate_device_key_pair()

        group.add_device(device_id, device_api_key)

        self.assertEqual(group.devices[0]["id"], device_id)

    def test_to_json(self):
        group = FLGroup("a_different_name", devices=[])

        device_id, device_api_key = generate_device_key_pair()

        group.add_device(device_id, device_api_key)

        json_data = group.to_json()

        self.assertTrue("ID" in json_data)
        self.assertTrue("devices" in json_data)
        self.assertEqual(len(json_data["devices"]), 1)
        self.assertTrue("rounds" in json_data)

    def test_from_json(self):
        json_data = {'name': 'a_different_name', 'ID': 1234556645443, 'devices': [{'id': 7640150571427383, 'api_key': '7e590298-a239-47e6-951a-e8558c3ef91b'}], 'rounds': []}

        group = FLGroup.from_json(json_data)

        self.assertEqual(group.get_name(), "a_different_name")
        self.assertEqual(group.get_id(), 1234556645443)
        self.assertEqual(group.get_rounds(), [])
        self.assertEqual(group.get_devices(), [{'id': 7640150571427383, 'api_key': '7e590298-a239-47e6-951a-e8558c3ef91b'}])

    def test_save_to_db(self):
        json_data = {'name': 'a_different_name', 'ID': 1234556645443, 'devices': [{'id': 7640150571427383, 'api_key': '7e590298-a239-47e6-951a-e8558c3ef91b'}], 'rounds': []}
        group = FLGroup.from_json(json_data)

        db_ = InMemoryDBInterface()

        self.assertTrue(FLGroup.save_to_db(group, db_))
        self.assertEqual(FLGroup.load_from_db(1234556645443, db_).to_json(), json_data)
