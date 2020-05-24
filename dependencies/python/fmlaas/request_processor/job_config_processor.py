from .request_processor import RequestProcessor
from ..model import JobConfiguration
from ..model.termination_criteria import DurationTerminationCriteria
from ..model.termination_criteria import get_termination_criteria_class_from_json
from ..utils import get_epoch_time

class JobConfigJSONProcessor(RequestProcessor):

    DEVICE_SELECTION_STRATEGY_KEY = "device_selection_strategy"
    NUM_DEVICES_KEY = "num_devices"
    NUM_BUFFER_DEVICES_KEY = "num_buffer_devices"
    TERMINATION_CRITERIA_KEY = "termination_criteria"

    def __init__(self, json):
        self.json = json

    def get_device_selection_strategy(self):
        device_selection_strategy = self.json.get(JobConfigJSONProcessor.DEVICE_SELECTION_STRATEGY_KEY, None)

        if not self._is_string_name_valid(device_selection_strategy):
            raise ValueError("Device selection strategy invalid.")

        return device_selection_strategy

    def get_num_devices(self):
        num_devices = self.json.get(JobConfigJSONProcessor.NUM_DEVICES_KEY, None)

        if not self._is_int_name_valid(num_devices):
            raise ValueError("Num devices invalid.")

        return num_devices

    def get_num_buffer_devices(self):
        num_buffer_devices = self.json.get(JobConfigJSONProcessor.NUM_BUFFER_DEVICES_KEY, None)

        if not self._is_int_name_valid(num_buffer_devices):
            raise ValueError("Num buffer devices invalid.")

        return num_buffer_devices

    def get_termination_criteria(self):
        termination_criteria = self.json.get(JobConfigJSONProcessor.TERMINATION_CRITERIA_KEY, None)

        if termination_criteria is None:
            raise ValueError("Termination criteria invalid.")

        converted_termination_criteria = []
        for criteria in termination_criteria:
            converted_termination_criteria.append(self._load_termination_criteria(criteria))

        return converted_termination_criteria

    def _load_termination_criteria(self, criteria):
        """
        :param criteria: dict
        """
        criteria_type = get_termination_criteria_class_from_json(criteria)
        if criteria_type == DurationTerminationCriteria:
            return DurationTerminationCriteria(criteria["max_duration_sec"],
                                               get_epoch_time())

        raise ValueError("Unknown termination criteria type")

    def generate_job_config(self):
        return JobConfiguration(self.get_num_devices(),
                                  self.get_num_buffer_devices(),
                                  self.get_device_selection_strategy(),
                                  [x.to_json() for x in self.get_termination_criteria()])
