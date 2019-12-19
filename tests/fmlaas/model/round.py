import unittest

from dependencies.python.fmlaas.model import Round
from dependencies.python.fmlaas.model import RoundStatus
from dependencies.python.fmlaas.model import Model

class RoundTestCase(unittest.TestCase):

    def test_to_json_pass(self):
        round = Round("my_id",
            ["test1", "test2"],
            RoundStatus.COMPLETED,
            "previous_round_id",
            {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : 2134235},
            {"config info" : "here"},
            {"test1" : {"size" : 123300}},
            "December 19th, 2019")

        round_json = round.to_json()

        self.assertEqual("my_id", round_json["ID"])
        self.assertEqual("COMPLETED", round_json["status"])
        self.assertEqual(["test1", "test2"], round_json["devices"])
        self.assertEqual("previous_round_id", round_json["previous_round_id"])
        self.assertEqual({"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : 2134235}, round_json["aggregate_model"])
        self.assertEqual({"config info" : "here"}, round_json["configuration"])
        self.assertEqual({"test1" : {"size" : 123300}}, round_json["models"])
        self.assertEqual("December 19th, 2019", round_json["created_on"])

    def test_from_json_pass(self):
        round_json = {'ID': 'my_id', 'status': 'COMPLETED', 'devices': ['test1', 'test2'], 'previous_round_id': 'previous_round_id', 'aggregate_model': {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : 2134235}, 'configuration': {'config info': 'here'}, 'models': {"123235345" : {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : 2134235}}, 'created_on': 'December 19th, 2019'}

        round = Round.from_json(round_json)

        self.assertEqual(round.get_id(), round_json["ID"])
        self.assertEqual(round.get_status(), RoundStatus.COMPLETED)
        self.assertEqual(round.get_devices(), round_json["devices"])
        self.assertEqual(round.get_previous_round_id(), round_json["previous_round_id"])
        self.assertEqual(round.get_aggregate_model().to_json(), round_json["aggregate_model"])
        self.assertEqual(round.get_configuration(), round_json["configuration"])
        self.assertEqual(round.get_models()["123235345"].to_json(), round_json["models"]["123235345"])
        self.assertEqual(round.get_created_on(), round_json["created_on"])

    def test_add_model_pass(self):
        round = Round("my_id",
            ["test1", "test2"],
            RoundStatus.COMPLETED,
            "previous_round_id",
            "aggregate_model",
            {"config info" : "here"},
            {},
            "December 19th, 2019")

        model = Model("12312312", "1234/2345/12312312", 234342324)

        round.add_model(model)

        self.assertTrue(model.get_entity_id() in round.models)
        self.assertTrue("12312312" in round.models[model.get_entity_id()]["name"])
        self.assertEqual(model.get_size(), round.models[model.get_entity_id()]["size"])

    def test_get_models(self):
        round = Round("my_id",
            ["test1", "test2"],
            RoundStatus.COMPLETED,
            "previous_round_id",
            {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : 2134235},
            {"config info" : "here"},
            {"123235345" : {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : 2134235}, "1232353465" : {"name" : "21313124/123123/1232353465", "entity_id" : "1232353465", "size" : 2134235}},
            "December 19th, 2019")

        models = round.get_models()

        self.assertEqual(len(models), 2)
        self.assertTrue("123235345" in models)
        self.assertTrue("1232353465" in models)

    def test_is_complete_pass_1(self):
        round = Round("my_id",
            ["test1", "test2"],
            RoundStatus.COMPLETED,
            "previous_round_id",
            {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : 2134235},
            {"config info" : "here"},
            {"123235345" : {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : 2134235}, "1232353465" : {"name" : "21313124/123123/1232353465", "entity_id" : "1232353465", "size" : 2134235}},
            "December 19th, 2019")

        self.assertTrue(round.is_complete())

    def test_is_complete_pass_2(self):
        round = Round("my_id",
            ["test1", "test2"],
            RoundStatus.IN_PROGRESS,
            "previous_round_id",
            {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : 2134235},
            {"config info" : "here"},
            {"123235345" : {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : 2134235}, "1232353465" : {"name" : "21313124/123123/1232353465", "entity_id" : "1232353465", "size" : 2134235}},
            "December 19th, 2019")

        self.assertFalse(round.is_complete())
