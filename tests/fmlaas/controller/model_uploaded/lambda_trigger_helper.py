import unittest

from dependencies.python.fmlaas.controller.model_uploaded import generate_aggregation_func_payload

class LambdaTriggerHelperTestCase(unittest.TestCase):

    def test_generate_aggregation_func_payload_pass(self):
        payload = generate_aggregation_func_payload("1234", "5678")

        self.assertEqual('{"group_id": "1234", "round_id": "5678"}', payload)
