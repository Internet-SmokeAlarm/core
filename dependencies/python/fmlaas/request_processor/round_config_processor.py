from .request_processor import RequestProcessor
from ..model import RoundConfiguration
from ..model.termination_criteria import DurationTerminationCriteria
from ..utils import get_epoch_time

class RoundConfigJSONProcessor(RequestProcessor):

    DEVICE_SELECTION_STRATEGY_KEY = "device_selection_strategy"
    NUM_DEVICES_KEY = "num_devices"
    NUM_BUFFER_DEVICES_KEY = "num_buffer_devices"
    TERMINATION_CRITERIA_KEY = "termination_criteria"

    def __init__(self, json):
        self.json = json

    def get_device_selection_strategy(self):
        device_selection_strategy = self.json.get(RoundConfigJSONProcessor.DEVICE_SELECTION_STRATEGY_KEY, None)

        if not self._is_string_name_valid(device_selection_strategy):
            raise ValueError("Device selection strategy invalid.")

        return device_selection_strategy

    def get_num_devices(self):
        num_devices = self.json.get(RoundConfigJSONProcessor.NUM_DEVICES_KEY, None)

        if not self._is_int_name_valid(num_devices):
            raise ValueError("Num devices invalid.")

        return num_devices

    def get_num_buffer_devices(self):
        num_buffer_devices = self.json.get(RoundConfigJSONProcessor.NUM_BUFFER_DEVICES_KEY, None)

        if not self._is_int_name_valid(num_buffer_devices):
            raise ValueError("Num buffer devices invalid.")

        return num_buffer_devices

    def get_termination_criteria(self):
        termination_criteria = self.json.get(RoundConfigJSONProcessor.TERMINATION_CRITERIA_KEY, None)

        if termination_criteria is None:
            raise ValueError("Termination criteria invalid.")

        converted_termination_criteria = []
        for criteria in termination_criteria:
            converted_termination_criteria.append(self._load_termination_criteria(criteria["type"], criteria))

        return converted_termination_criteria

    def _load_termination_criteria(self, criteria_type, criteria):
        """
        :param criteria_type: string
        :param criteria: dict
        """
        if criteria_type == "duration":
            return DurationTerminationCriteria(criteria["max_duration_sec"],
                                               get_epoch_time())

        raise ValueError("Unknown termination criteria type")

    def generate_round_config(self):
        return RoundConfiguration(self.get_num_devices(),
                                  self.get_num_buffer_devices(),
                                  self.get_device_selection_strategy(),
                                  [x.to_json() for x in self.get_termination_criteria()])
