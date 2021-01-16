from typing import List

from ..model import JobConfiguration
from ..model.device_selection_strategy import DeviceSelectionStrategy
from ..model.termination_criteria import get_termination_criteria_from_json
from ..model.termination_criteria.termination_criteria import \
    TerminationCriteria
from .request_processor import RequestProcessor


class JobConfigJSONProcessor(RequestProcessor):

    DEVICE_SELECTION_STRATEGY_KEY = "device_selection_strategy"
    NUM_DEVICES_KEY = "num_devices"
    NUM_BACKUP_DEVICES_KEY = "num_backup_devices"
    TERMINATION_CRITERIA_KEY = "termination_criteria"

    def __init__(self, json):
        self.json = json

    def get_device_selection_strategy(self) -> DeviceSelectionStrategy:
        device_selection_strategy = self.json.get(
            JobConfigJSONProcessor.DEVICE_SELECTION_STRATEGY_KEY, None)

        if not self._is_string_name_valid(device_selection_strategy):
            raise ValueError("Device selection strategy invalid.")

        return DeviceSelectionStrategy(device_selection_strategy)

    def get_num_devices(self) -> int:
        num_devices = self.json.get(
            JobConfigJSONProcessor.NUM_DEVICES_KEY, None)

        print(num_devices)
        if not self._is_int_name_valid(num_devices):
            raise ValueError("Num devices invalid.")
        print("WTF")

        return int(num_devices)

    def get_num_backup_devices(self) -> int:
        num_backup_devices = self.json.get(
            JobConfigJSONProcessor.NUM_BACKUP_DEVICES_KEY, None)

        if not self._is_int_name_valid(num_backup_devices):
            raise ValueError("Num backup devices invalid.")

        return int(num_backup_devices)

    def get_termination_criteria(self) -> List[TerminationCriteria]:
        termination_criteria = self.json.get(
            JobConfigJSONProcessor.TERMINATION_CRITERIA_KEY, None)

        if termination_criteria is None:
            raise ValueError("Termination criteria invalid.")

        converted_termination_criteria = []
        for criteria in termination_criteria:
            converted_termination_criteria.append(
                get_termination_criteria_from_json(criteria))

        return converted_termination_criteria

    def generate_job_config(self) -> JobConfiguration:
        print(self.get_num_devices())
        print(self.get_num_backup_devices())
        print(self.get_device_selection_strategy())
        print(self.get_termination_criteria())

        return JobConfiguration(self.get_num_devices(),
                                self.get_num_backup_devices(),
                                self.get_device_selection_strategy(),
                                self.get_termination_criteria())
