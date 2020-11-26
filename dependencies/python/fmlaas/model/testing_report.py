from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TestingReport:

    confusion_matrix: List[List[int]]
    accuracy: float
    loss: float
    device_id: str

    def to_json(self) -> dict:
        return {
            "device_id": self.device_id,
            "confusion_matrix": self.confusion_matrix,
            "accuracy": self.accuracy,
            "loss": self.loss
        }

    @staticmethod
    def from_json(data: dict):
        return TestingReport(data["confusion_matrix"],
                             data["accuracy"],
                             data["loss"],
                             data["device_id"])
