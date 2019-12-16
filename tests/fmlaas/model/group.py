import unittest

from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas import generate_device_key_pair
from dependencies.python.fmlaas import generate_unique_id
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas import HierarchicalModelNameStructure

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

    def test_save_to_load_from_db_1(self):
        json_data = {'name': 'a_different_name', 'ID': 1234556645443, 'devices': [{'id': 7640150571427383, 'api_key': '7e590298-a239-47e6-951a-e8558c3ef91b'}], 'rounds': []}
        group = FLGroup.from_json(json_data)

        db_ = InMemoryDBInterface()

        self.assertTrue(FLGroup.save_to_db(group, db_))
        self.assertEqual(FLGroup.load_from_db(1234556645443, db_).to_json(), json_data)

    def test_save_to_load_from_db_2(self):
        json_data = {'name': 'a_different_name', 'ID': 1234556645443, 'devices': [{'id': 7640150571427383, 'api_key': '7e590298-a239-47e6-951a-e8558c3ef91b'}], 'rounds': [{'id': 7420988340570048, 'models': ['test_model_1']}]}
        group = FLGroup.from_json(json_data)

        db_ = InMemoryDBInterface()

        self.assertTrue(FLGroup.save_to_db(group, db_))
        self.assertEqual(FLGroup.load_from_db(1234556645443, db_).to_json(), json_data)

    def test_create_round(self):
        group = FLGroup("a_different_name", devices=[], rounds=[])

        round_id = generate_unique_id()

        group.create_round(round_id)

        json_data = group.to_json()

        self.assertTrue("ID" in json_data)
        self.assertTrue("devices" in json_data)
        self.assertEqual(len(json_data["devices"]), 0)
        self.assertTrue("rounds" in json_data)
        self.assertEqual(len(json_data["rounds"]), 1)

    def test_add_model_to_group_device_update(self):
        group = FLGroup("a_different_name", devices=[], rounds=[])

        round_id = generate_unique_id()

        model_name_txt = "1234/" + str(round_id) + "/9999"

        model_name = HierarchicalModelNameStructure()
        model_name.load_name(model_name_txt)

        group.create_round(round_id)
        group.add_model_to_group(model_name)

        json_data = group.to_json()

        self.assertEqual(json_data["rounds"][0]["id"], round_id)
        self.assertTrue(9999 in json_data["rounds"][0]["models"])

    def test_add_model_to_group_round_aggregate_model(self):
        group = FLGroup("a_different_name", devices=[], rounds=[])

        round_id = generate_unique_id()

        model_name_txt = "1234/" + str(round_id) + "/" + str(round_id)

        model_name = HierarchicalModelNameStructure()
        model_name.load_name(model_name_txt)

        group.create_round(round_id)
        group.add_model_to_group(model_name)

        json_data = group.to_json()

        self.assertEqual(json_data["rounds"][0]["id"], round_id)
        self.assertEqual(round_id, json_data["rounds"][0]["combined_model"])

    def test_add_model_to_group_initial_group_model(self):
        group = FLGroup("a_different_name", id=1234, devices=[], rounds=[])

        model_name_txt = "1234/1234"

        model_name = HierarchicalModelNameStructure()
        model_name.load_name(model_name_txt)

        group.add_model_to_group(model_name)

        json_data = group.to_json()

        self.assertEqual(group.get_initial_model(), json_data["ID"])

    def test_add_model_to_round_1(self):
        group = FLGroup("a_different_name", devices=[], rounds=[])

        round_id = generate_unique_id()

        group.create_round(round_id)
        group.add_model_to_round(round_id, "test_model_1")

        json_data = group.to_json()

        self.assertEqual(json_data["rounds"][0]["id"], round_id)
        self.assertTrue("test_model_1" in json_data["rounds"][0]["models"])

    def test_add_model_to_round_2(self):
        group = FLGroup("a_different_name", devices=[], rounds=[])

        round_id = generate_unique_id()
        round_id_2 = generate_unique_id()

        group.create_round(round_id)
        group.create_round(round_id_2)
        group.add_model_to_round(round_id, "test_model_1")

        json_data = group.to_json()

        self.assertEqual(len(json_data["rounds"]), 2)
        self.assertEqual(json_data["rounds"][0]["id"], round_id)
        self.assertEqual(json_data["rounds"][1]["id"], round_id_2)
        self.assertTrue("test_model_1" in json_data["rounds"][0]["models"])

    def test_add_duplicate_model_to_round(self):
        group = FLGroup("a_different_name", devices=[], rounds=[])

        round_id = generate_unique_id()
        round_id_2 = generate_unique_id()

        group.create_round(round_id)
        group.add_model_to_round(round_id, "test_model_1")
        group.add_model_to_round(round_id, "test_model_1")

        json_data = group.to_json()

        self.assertTrue("test_model_1" in json_data["rounds"][0]["models"])
        self.assertEqual(1, len(json_data["rounds"][0]["models"]))

    def test_get_round(self):
        group = FLGroup("a_different_name", devices=[], rounds=[])

        round_id = generate_unique_id()
        round_id_2 = generate_unique_id()

        group.create_round(round_id)
        group.create_round(round_id_2)
        group.add_model_to_round(round_id, "test_model_1")

        round_json = group.get_round(round_id)
        round_2_json = group.get_round(round_id_2)

        self.assertEqual(round_json["id"], round_id)
        self.assertEqual(round_2_json["id"], round_id_2)
        self.assertEqual(len(round_json["models"]), 1)
        self.assertEqual(len(round_2_json["models"]), 0)

    def test_get_models(self):
        group = FLGroup("a_different_name", devices=[], rounds=[])

        round_id = generate_unique_id()
        round_id_2 = generate_unique_id()

        group.create_round(round_id)
        group.create_round(round_id_2)
        group.add_model_to_round(round_id, "test_model_1")

        round_models = group.get_models(round_id)
        round_models_2 = group.get_models(round_id_2)

        self.assertEqual(len(round_models), 1)
        self.assertEqual(len(round_models_2), 0)
        self.assertEqual(round_models[0], "test_model_1")

    def test_set_round_global_model(self):
        group = FLGroup("a_different_name", devices=[], rounds=[])

        round_id = generate_unique_id()
        round_id_2 = generate_unique_id()

        group.create_round(round_id)
        group.create_round(round_id_2)
        group.set_round_global_model(round_id, "test_model_1")

        round_json = group.get_round(round_id)
        round_2_json = group.get_round(round_id_2)

        self.assertEqual(round_json["id"], round_id)
        self.assertEqual(round_2_json["id"], round_id_2)
        self.assertEqual(round_2_json["combined_model"], "N/A")
        self.assertEqual(round_json["combined_model"], "test_model_1")
