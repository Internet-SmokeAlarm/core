import unittest

from dependencies.python.fmlaas.utils import get_epoch_time
from dependencies.python.fmlaas.model.termination_criteria import DurationTerminationCriteria

class DurationTerminationCriteriaTestCase(unittest.TestCase):

    def test_criteria_satisfied_pass_true(self):
        criteria = DurationTerminationCriteria(100, float(get_epoch_time()) - 100.0)

        self.assertTrue(criteria.is_criteria_satisfied(None))

    def test_criteria_satisfied_pass_false(self):
        criteria = DurationTerminationCriteria(100, float(get_epoch_time()) - 50.0)

        self.assertFalse(criteria.is_criteria_satisfied(None))

    def test_from_json_pass(self):
        criteria_json = {
            "type" : "DurationTerminationCriteria",
            "max_duration_sec" : "100",
            "start_epoch_time" : "1235345.5234"
        }
        criteria = DurationTerminationCriteria.from_json(criteria_json)

        self.assertEqual(criteria.get_max_duration_sec(), 100)
        self.assertEqual(criteria.get_start_epoch_time(), 1235345.5234)

    def test_to_json_pass(self):
        criteria = DurationTerminationCriteria(100, 1235345.5234)
        criteria_json = {
            "type" : "DurationTerminationCriteria",
            "max_duration_sec" : "100",
            "start_epoch_time" : "1235345.5234"
        }

        self.assertEqual(criteria.to_json(), criteria_json)
