import unittest

from dependencies.python.fmlaas.request_processor import TestingReportProcessor


class TestingReportTestCase(unittest.TestCase):

    def test_get_accuracy_fail(self):
        json_data = {"accuracy": "None"}
        testing_report_processor = TestingReportProcessor(json_data)

        self.assertRaises(ValueError, testing_report_processor.get_accuracy)

    def test_get_accuracy_fail_2(self):
        json_data = {"accuracy": 1234}
        testing_report_processor = TestingReportProcessor(json_data)

        self.assertRaises(ValueError, testing_report_processor.get_accuracy)

    def test_get_accuracy_fail_3(self):
        json_data = {}
        testing_report_processor = TestingReportProcessor(json_data)

        self.assertRaises(ValueError, testing_report_processor.get_accuracy)

    def test_get_accuracy_pass(self):
        json_data = {"accuracy": 81.34}
        testing_report_processor = TestingReportProcessor(json_data)

        self.assertEqual(81.34, testing_report_processor.get_accuracy())

    def test_get_loss_fail(self):
        json_data = {"loss": None}
        testing_report_processor = TestingReportProcessor(json_data)

        self.assertRaises(ValueError, testing_report_processor.get_loss)

    def test_get_loss_fail_2(self):
        json_data = {"loss": "12334"}
        testing_report_processor = TestingReportProcessor(json_data)

        self.assertRaises(ValueError, testing_report_processor.get_loss)

    def test_get_loss_fail_3(self):
        testing_report_processor = TestingReportProcessor({})
        self.assertIsNone(testing_report_processor.get_loss(throw_exception=False))

    def test_get_loss_pass(self):
        json_data = {"loss": 2.3}
        testing_report_processor = TestingReportProcessor(json_data)

        self.assertEqual(2.3, testing_report_processor.get_loss())

    def test_get_confusion_matrix_fail(self):
        json_data = {"confusion_matrix": None}
        testing_report_processor = TestingReportProcessor(json_data)

        self.assertRaises(ValueError, testing_report_processor.get_confusion_matrix)

    def test_get_confusion_matrix_fail_2(self):
        json_data = {"confusion_matrix": 12334}
        testing_report_processor = TestingReportProcessor(json_data)

        self.assertRaises(ValueError, testing_report_processor.get_confusion_matrix)

    def test_get_confusion_matrix_fail_3(self):
        testing_report_processor = TestingReportProcessor({})
        self.assertIsNone(testing_report_processor.get_confusion_matrix(throw_exception=False))

    def test_get_confusion_matrix_pass(self):
        json_data = {"confusion_matrix": [[10, 0, 0], [0, 10, 0], [0, 0, 10]]}
        testing_report_processor = TestingReportProcessor(json_data)

        self.assertEqual([[10, 0, 0], [0, 10, 0], [0, 0, 10]], testing_report_processor.get_confusion_matrix())

    def test_generate_testing_report_pass(self):
        json_data = {
            "accuracy": 83.43,
            "loss": 10.3,
            "confusion_matrix": [[10, 0, 0], [0, 10, 0], [0, 0, 10]]
        }
        testing_report_processor = TestingReportProcessor(json_data)

        generated_testing_report = testing_report_processor.generate_testing_report("dsfs234fasf23d23sfg342bf")
        correct_testing_report = TestingReport([[10, 0, 0], [0, 10, 0], [0, 0, 10]], 83.43, 10.3, "dsfs234fasf23d23sfg342bf")

        self.assertEqual(generated_testing_report, correct_testing_report)
