import unittest

from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.model import Round
from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import RoundConfiguration
from dependencies.python.fmlaas import generate_device_key_pair
from dependencies.python.fmlaas import generate_unique_id
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas import HierarchicalModelNameStructure

class FLGroupTestCase(unittest.TestCase):

    def test_add_device_pass(self):
        group = FLGroup("my_name", "id", {}, {})

        device_id, device_api_key = generate_device_key_pair()

        group.add_device(device_id)

        self.assertTrue(device_id in group.get_devices())

    def test_to_json_pass(self):
        group = FLGroup("a_different_name", "id", {}, {})

        device_id, device_api_key = generate_device_key_pair()

        group.add_device(device_id)

        json_data = group.to_json()

        self.assertTrue("ID" in json_data)
        self.assertTrue("devices" in json_data)
        self.assertEqual(len(json_data["devices"]), 1)
        self.assertTrue("rounds" in json_data)

    def test_to_json_pass_2(self):
        group = FLGroup("a_different_name", "id", {}, {})

        device_id, device_api_key = generate_device_key_pair()
        group.add_device(device_id)

        device_id_2, device_api_key = generate_device_key_pair()
        group.add_device(device_id_2)

        json_data = group.to_json()

        self.assertTrue("ID" in json_data)
        self.assertTrue("devices" in json_data)
        self.assertEqual(len(json_data["devices"]), 2)
        self.assertTrue("rounds" in json_data)

    def test_from_json_pass(self):
        json_data = {'name': 'a_different_name', 'ID': 'id', 'devices': {'6617961791227642': {'ID': '6617961791227642', 'registered_on': 1576779269.11093}, '6336011475872533': {'ID': '6336011475872533', 'registered_on': 1576779269.110966}}, 'rounds': {}}

        group = FLGroup.from_json(json_data)

        self.assertEqual(group.get_name(), "a_different_name")
        self.assertEqual(group.get_id(), "id")
        self.assertEqual(group.get_rounds(), {})
        self.assertEqual(group.get_devices(), {'6617961791227642': {'ID': '6617961791227642', 'registered_on': 1576779269.11093}, '6336011475872533': {'ID': '6336011475872533', 'registered_on': 1576779269.110966}})

    def test_from_json_pass_2(self):
        json_data = {'name': 'a_different_name', 'ID': 'id10', 'devices': {'7897956979947357': {'ID': '7897956979947357', 'registered_on': 1576779498.189228}, '1822867963788927': {'ID': '1822867963788927', 'registered_on': 1576779498.189258}}, 'rounds': {'4152602852358113': {'ID': '4152602852358113', 'status': 'IN_PROGRESS', 'devices': ['7897956979947357', '1822867963788927'], 'previous_round_id': 'N/A', 'aggregate_model': 'N/A', 'configuration': {'num_devices': 50}, 'models': {}, 'created_on': 1576779498.189267}}}

        group = FLGroup.from_json(json_data)

        self.assertEqual(group.get_name(), "a_different_name")
        self.assertEqual(group.get_id(), "id10")
        self.assertEqual(group.get_rounds(), {'4152602852358113': {'ID': '4152602852358113', 'status': 'IN_PROGRESS', 'devices': ['7897956979947357', '1822867963788927'], 'previous_round_id': 'N/A', 'aggregate_model': 'N/A', 'configuration': {'num_devices': 50}, 'models': {}, 'created_on': 1576779498.189267}})
        self.assertEqual(group.get_devices(), {'7897956979947357': {'ID': '7897956979947357', 'registered_on': 1576779498.189228}, '1822867963788927': {'ID': '1822867963788927', 'registered_on': 1576779498.189258}})

    def test_save_to_load_from_db_1(self):
        json_data = {'name': 'a_different_name', 'ID': 'id', 'devices': {'6617961791227642': {'ID': '6617961791227642', 'registered_on': 1576779269.11093}, '6336011475872533': {'ID': '6336011475872533', 'registered_on': 1576779269.110966}}, 'rounds': {}}
        group = FLGroup.from_json(json_data)

        db_ = InMemoryDBInterface()

        self.assertTrue(group.save_to_db(db_))
        self.assertEqual(FLGroup.load_from_db("id", db_).to_json(), json_data)

    def test_save_to_load_from_db_2(self):
        json_data = {'name': 'a_different_name', 'ID': 'id10', 'devices': {'7897956979947357': {'ID': '7897956979947357', 'registered_on': 1576779498.189228}, '1822867963788927': {'ID': '1822867963788927', 'registered_on': 1576779498.189258}}, 'rounds': {'4152602852358113': {'ID': '4152602852358113', 'status': 'IN_PROGRESS', 'devices': ['7897956979947357', '1822867963788927'], 'previous_round_id': 'N/A', 'aggregate_model': 'N/A', 'configuration': {'num_devices': 50}, 'models': {}, 'created_on': 1576779498.189267}}}
        group = FLGroup.from_json(json_data)

        db_ = InMemoryDBInterface()

        self.assertTrue(group.save_to_db(db_))
        self.assertEqual(FLGroup.load_from_db('id10', db_).to_json(), json_data)

    def test_add_round_pass(self):
        group = FLGroup("a_different_name", "id", {}, {})

        round_id = generate_unique_id()
        builder = RoundBuilder()
        builder.set_id(round_id)

        builder.set_configuration(RoundConfiguration(50).to_json())
        round = builder.build()

        group.add_round(round)

        self.assertTrue(round_id in group.rounds)

    def test_create_round_pass(self):
        group = FLGroup("a_different_name", "id", {}, {})

        round_id = group.create_round(RoundConfiguration(50))

        self.assertTrue(round_id in group.rounds)

    def test_add_model_device_update(self):
        group = FLGroup("a_different_name", "id", {}, {})

        round_config = RoundConfiguration(50)
        round_id = group.create_round(round_config)
        model_name_txt = "1234/" + round_id + "/9999"
        model = Model(None, model_name_txt, 123134)

        group.add_model(model)

        json_data = group.to_json()

        self.assertTrue(round_id in json_data["rounds"])
        self.assertTrue("9999" in json_data["rounds"][round_id]["models"])

    def test_add_model_round_aggregate_model(self):
        group = FLGroup("a_different_name", "id", {}, {})

        round_config = RoundConfiguration(50)
        round_id = group.create_round(round_config)
        model_name_txt = "1234/" + round_id + "/" + round_id

        model = Model(None, model_name_txt, 123134)

        group.add_model(model)

        json_data = group.to_json()

        self.assertTrue(round_id in json_data["rounds"])
        self.assertEqual(round_id, json_data["rounds"][round_id]["aggregate_model"]["entity_id"])

    def test_add_model_initial_group_model(self):
        group = FLGroup("a_different_name", "1234", {}, {})

        model_name_txt = "1234/1234"
        model = Model(None, model_name_txt, 123134)

        group.add_model(model)

        json_data = group.to_json()

        self.assertEqual(group.get_initial_model(), json_data["ID"])

    def test_add_model_to_round(self):
        group = FLGroup("a_different_name", "id", {}, {})

        round_config = RoundConfiguration(50)
        round_id = group.create_round(round_config)

        model_name_txt = "1234/" + round_id + "/9999"
        model = Model("9999", model_name_txt, 123134)

        group.add_model_to_round(round_id, model)

        json_data = group.to_json()

        self.assertTrue(round_id in json_data["rounds"])
        self.assertTrue("9999" in json_data["rounds"][round_id]["models"])

    def test_add_duplicate_model_to_round(self):
        group = FLGroup("a_different_name", "id", {}, {})

        round_id = group.create_round(RoundConfiguration(50))
        group.add_model_to_round(round_id, Model("123123123124", "1234/3456/123123123124", 123123))
        group.add_model_to_round(round_id, Model("123123123124", "1234/3456/123123123124", 345346))

        json_data = group.to_json()

        self.assertTrue("123123123124" in json_data["rounds"][round_id]["models"])
        self.assertEqual(1, len(json_data["rounds"][round_id]["models"]))

    def test_get_round(self):
        group = FLGroup("a_different_name", "id", {}, {})

        round_id = group.create_round(RoundConfiguration(50))
        round_id_2 = group.create_round(RoundConfiguration(50))
        group.add_model_to_round(round_id, Model("1234", "3445/55665/1234", 12345))

        round = group.get_round(round_id)
        round_2 = group.get_round(round_id_2)

        self.assertEqual(round.get_id(), round_id)
        self.assertEqual(round_2.get_id(), round_id_2)
        self.assertEqual(len(round.get_models()), 1)
        self.assertEqual(len(round_2.get_models()), 0)

    def test_contains_round_pass(self):
        group = FLGroup("a_different_name", "id", {}, {})

        round_id = group.create_round(RoundConfiguration(50))

        self.assertTrue(group.contains_round(round_id))

    def test_contains_round_fail(self):
        group = FLGroup("a_different_name", "id", {}, {})

        round_id = group.create_round(RoundConfiguration(500))
        round_id_2 = "i_dont_exist"

        self.assertFalse(group.contains_round(round_id_2))

    def test_get_models(self):
        group = FLGroup("a_different_name", "id", {}, {})

        round_id = group.create_round(RoundConfiguration(50))
        round_id_2 = group.create_round(RoundConfiguration(50))
        group.add_model_to_round(round_id, Model("1234", "2345/34456/1234", 14345))

        round_models = group.get_models(round_id)
        round_models_2 = group.get_models(round_id_2)

        self.assertEqual(len(round_models), 1)
        self.assertEqual(len(round_models_2), 0)
        self.assertEqual(round_models["1234"].get_entity_id(), "1234")

    def test_set_round_global_model(self):
        group = FLGroup("a_different_name", "id", {}, {})

        round_id = group.create_round(RoundConfiguration(50))
        round_id_2 = group.create_round(RoundConfiguration(50))
        group.set_round_aggregate_model(round_id, Model("1234", "3455/1234/1234", 123155))

        round = group.get_round(round_id)
        round_2 = group.get_round(round_id_2)

        self.assertEqual(round_id, round.get_id())
        self.assertEqual(round_id_2, round_2.get_id())
        self.assertEqual(Model("1234", "3455/1234/1234", 123155).to_json(), round.get_aggregate_model().to_json())
