import unittest
from dependencies.python.fmlaas.model import TestingReport


class TestingReportTestCase(unittest.TestCase):

    def test_to_json_pass(self):
        testing_report = TestingReport([[10, 0, 0], [0, 10, 0], [0, 0, 10]], 88.44, 2.454, "12124325adfdsfa2radfads234r")

        testing_report_json = testing_report.to_json()
        correct_json = {
            "confusion_matrix": [[10, 0, 0], [0, 10, 0], [0, 0, 10]],
            "accuracy": 88.44,
            "loss": 2.454,
            "device_id": "12124325adfdsfa2radfads234r"
        }

        self.assertEqual(correct_json, testing_report_json)

    def test_from_json_pass(self):
        correct_testing_report = TestingReport([[10, 0, 0], [0, 10, 0], [0, 0, 10]], 88.44, 2.454, "12124325adfdsfa2radfads234r")
        testing_report_json = {
            "confusion_matrix": [[10, 0, 0], [0, 10, 0], [0, 0, 10]],
            "accuracy": 88.44,
            "loss": 2.454,
            "device_id": "12124325adfdsfa2radfads234r"
        }

        self.assertEqual(correct_testing_report, TestingReport.from_json(testing_report_json))
