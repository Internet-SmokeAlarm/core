from typing import List

from .device_selection_strategy import DeviceSelectionStrategy
from .termination_criteria import (TerminationCriteria,
                                   save_termination_criteria_to_json,
                                   load_termination_criteria_from_json)


class JobConfiguration:

    def __init__(self,
                 num_devices: int,
                 num_backup_devices: int,
                 device_selection_strategy: DeviceSelectionStrategy,
                 termination_criteria: List[TerminationCriteria]):
        self._num_devices = num_devices
        self._num_backup_devices = num_backup_devices
        self._device_selection_strategy = device_selection_strategy
        self._termination_criteria = termination_criteria

    @property
    def num_devices(self) -> int:
        return self._num_devices

    @property
    def num_backup_devices(self) -> int:
        return self._num_backup_devices
    
    @property
    def device_selection_strategy(self) -> DeviceSelectionStrategy:
        return self._device_selection_strategy

    @property
    def termination_criteria(self) -> List[TerminationCriteria]:
        return self._termination_criteria
    
    @termination_criteria.setter
    def termination_criteria(self, termination_criteria: List[TerminationCriteria]) -> None:
        self._termination_criteria = list()
        for criteria in termination_criteria:
            self._termination_criteria.append(criteria)

    def get_total_num_devices(self) -> int:
        return self._num_devices + self._num_backup_devices

    def add_termination_criteria(self, termination_criteria: TerminationCriteria) -> None:
        self._termination_criteria.append(termination_criteria)

    def reset_termination_criteria(self) -> None:
        updated_criteria = list()
        for criteria in self._termination_criteria:
            criteria.reset()

            updated_criteria.append(criteria)

        self._termination_criteria = updated_criteria

    def to_json(self) -> dict:
        return {
            "num_devices": str(self._num_devices),
            "num_backup_devices": str(self._num_backup_devices),
            "device_selection_strategy": self._device_selection_strategy.value,
            "termination_criteria": save_termination_criteria_to_json(self._termination_criteria)
        }

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and \
            (self._num_devices == other._num_devices) and \
            (self._num_backup_devices == other._num_backup_devices) and \
            (self._device_selection_strategy == other._device_selection_strategy) and \
            (self._termination_criteria == other._termination_criteria)

    @staticmethod
    def from_json(json_data):
        return JobConfiguration(int(json_data["num_devices"]),
                                int(json_data["num_backup_devices"]),
                                DeviceSelectionStrategy(json_data["device_selection_strategy"]),
                                load_termination_criteria_from_json(json_data["termination_criteria"]))
