import unittest

from dependencies.python.fmlaas.model.termination_criteria import get_termination_criteria_from_json
from dependencies.python.fmlaas.model.termination_criteria import get_termination_criteria_class_from_json
from dependencies.python.fmlaas.model.termination_criteria import DurationTerminationCriteria


class TerminationCriteriaUtilsTestCase(unittest.TestCase):

    def test_get_termination_criteria_from_json_pass_1(self):
        criteria_json = {
            "type": "DurationTerminationCriteria",
            "max_duration_sec": "100",
            "start_epoch_time": "1235345.5234"
        }

        criteria = get_termination_criteria_from_json(criteria_json)

        self.assertEqual(criteria.__class__, DurationTerminationCriteria)
        self.assertEqual(criteria.get_max_duration_sec(), 100)
        self.assertEqual(criteria.get_start_epoch_time(), 1235345.5234)

    def test_get_termination_criteria_from_json_fail_1(self):
        criteria_json = {
            "type": "NonexistantCriteriaClassName",
            "max_duration_sec": "100",
            "start_epoch_time": "1235345.5234"
        }

        self.assertRaises(
            ValueError,
            get_termination_criteria_from_json,
            criteria_json)

    def test_get_termination_criteria_class_from_json(self):
        criteria_json = {
            "type": "DurationTerminationCriteria"
        }

        criteria_class = get_termination_criteria_class_from_json(
            criteria_json)

        self.assertEqual(criteria_class, DurationTerminationCriteria)

    def test_get_termination_criteria_class_from_json_fail_1(self):
        criteria_json = {
            "type": "none_of_the_ones"
        }

        self.assertRaises(
            ValueError,
            get_termination_criteria_class_from_json,
            criteria_json)
