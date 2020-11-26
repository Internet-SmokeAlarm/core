from dependencies.python.fmlaas.model import Model

from .abstract_model_testcase import AbstractModelTestCase


class ModelTestCase(AbstractModelTestCase):

    def test_to_json_pass(self):
        model, json_repr = self._create_model()

        self.assertEqual(model.to_json(), json_repr)

    def test_from_json_pass(self):
        orig_model, json_repr = self._create_model()

        model = Model.from_json(json_repr)

        self.assertEqual(model, orig_model)

    def test_is_valid_json_pass(self):
        self.assertTrue(Model.is_valid_json(
            {'entity_id': '1234', 'name': '4456/5567/1234', 'size': "123552"}))
        self.assertFalse(Model.is_valid_json(
            {'name': '4456/5567/1234', 'size': "123552"}))
        self.assertFalse(Model.is_valid_json(
            {'entity_id': '1234', 'size': "123552"}))
        self.assertFalse(Model.is_valid_json(
            {'entity_id': '1234', 'name': '4456/5567/1234'}))

    def test_eq_pass(self):
        model_1 = Model("123123", "23123/123123/1231231", "12312313")
        model_2 = Model("564543", "23123/123123/1231231", "12312313")
        model_3 = Model("564543", "23123/123123/1231231", "12312313")
        model_4 = Model("564543", "23123/123123/1231231", "123512313")

        self.assertTrue(model_1 == model_1)
        self.assertFalse(model_1 == model_2)
        self.assertTrue(model_2 == model_3)
        self.assertFalse(model_2 == model_4)
