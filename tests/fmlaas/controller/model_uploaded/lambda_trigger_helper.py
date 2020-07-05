import unittest

from dependencies.python.fmlaas.controller.model_uploaded import generate_aggregation_func_payload


class LambdaTriggerHelperTestCase(unittest.TestCase):

    def test_generate_aggregation_func_payload_pass(self):
        payload = generate_aggregation_func_payload("1234", "76543", "5678")

        self.assertEqual('{"project_id": "1234", "experiment_id": "76543", "job_id": "5678"}', payload)
