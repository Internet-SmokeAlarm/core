import unittest

from dependencies.python.fmlaas.model.termination_criteria import \
    DurationTerminationCriteria
from dependencies.python.fmlaas.utils import get_epoch_time


class DurationTerminationCriteriaTestCase(unittest.TestCase):

    def test_criteria_satisfied_pass_true(self):
        criteria = DurationTerminationCriteria(
            100, get_epoch_time() - 100)

        self.assertTrue(criteria.is_criteria_satisfied())

    def test_criteria_satisfied_pass_false(self):
        criteria = DurationTerminationCriteria(
            100, get_epoch_time() - 50)

        self.assertFalse(criteria.is_criteria_satisfied())

    def test_from_json_pass(self):
        criteria_json = {
            "type": "DurationTerminationCriteria",
            "max_duration_sec": "100",
            "start_epoch_time": "1235345"
        }
        criteria = DurationTerminationCriteria.from_json(criteria_json)

        self.assertEqual(criteria.max_duration_sec, 100)
        self.assertEqual(criteria.start_epoch_time, 1235345)
    
    def test_from_json_pass_no_start_epoch_time(self):
        criteria_json = {
            "type": "DurationTerminationCriteria",
            "max_duration_sec": "100"
        }
        criteria = DurationTerminationCriteria.from_json(criteria_json)

        self.assertEqual(criteria.max_duration_sec, 100)
        self.assertIsNotNone(criteria.start_epoch_time)

    def test_to_json_pass(self):
        criteria = DurationTerminationCriteria(100, 1235345)
        criteria_json = {
            "type": "DurationTerminationCriteria",
            "max_duration_sec": "100",
            "start_epoch_time": "1235345"
        }

        self.assertEqual(criteria.to_json(), criteria_json)

    def test_reset_pass(self):
        start_epoch_time = get_epoch_time() - 100
        criteria = DurationTerminationCriteria(100, start_epoch_time)
        criteria.reset()

        self.assertNotEqual(criteria.start_epoch_time, start_epoch_time)
