import unittest

from dependencies.python.fmlaas.model import Model

class ModelTestCase(unittest.TestCase):

    def test_to_json_pass(self):
        model = Model("1234", "4456/5567/1234", "123552")

        json_data = model.to_json()

        self.assertEqual(model.get_entity_id(), json_data["entity_id"])
        self.assertEqual("4456/5567/1234", json_data["name"])
        self.assertEqual(model.get_size(), json_data["size"])

    def test_from_json_pass(self):
        json_data = {'entity_id': '1234', 'name': '4456/5567/1234', 'size': "123552"}

        model = Model.from_json(json_data)

        self.assertEqual(model.get_entity_id(), "1234")
        self.assertEqual(model.get_name().get_name(), "4456/5567/1234")
        self.assertEqual(model.get_size(), "123552")
