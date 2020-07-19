from .request_processor import RequestProcessor
from ..model import TestingReport
from typing import List


class TestingReportProcessor(RequestProcessor):

    ACCURACY_KEY = "accuracy"
    CONFUSION_MATRIX_KEY = "confusion_matrix"
    LOSS_KEY = "loss"

    def __init__(self, json: dict):
        self.json = json

    def get_accuracy(self, throw_exception=True) -> float:
        accuracy = self.json.get(TestingReportProcessor.ACCURACY_KEY, None)

        if not self._is_float_valid(accuracy) and throw_exception:
            raise ValueError("Accuracy invalid.")

        return accuracy

    def get_confusion_matrix(self, throw_exception=True) -> List[List[int]]:
        confusion_matrix = self.json.get(TestingReportProcessor.CONFUSION_MATRIX_KEY, None)

        if type(confusion_matrix) != type([]) and throw_exception:
            raise ValueError("Confusion matrix invalid.")

        return confusion_matrix

    def get_loss(self, throw_exception=True) -> float:
        loss = self.json.get(TestingReportProcessor.LOSS_KEY, None)

        if not self._is_float_valid(loss) and throw_exception:
            raise ValueError("Loss invalid.")

        return loss

    def generate_testing_report(self, device_id: str) -> TestingReport:
        return TestingReport(self.get_confusion_matrix(),
                             self.get_accuracy(),
                             self.get_loss(),
                             device_id)
