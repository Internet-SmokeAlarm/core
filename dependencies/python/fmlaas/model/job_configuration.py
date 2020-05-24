from .termination_criteria import get_termination_criteria_from_json


class JobConfiguration:

    def __init__(self, num_devices, num_buffer_devices,
                 device_selection_strategy, termination_criteria):
        """
        :param num_devices: int
        :param num_buffer_devices: int
        :param device_selection_strategy: string
        :param termination_criteria: list(dict)
        """
        self.num_devices = num_devices
        self.num_buffer_devices = num_buffer_devices
        self.device_selection_strategy = device_selection_strategy
        self.termination_criteria = termination_criteria

    def get_num_devices(self):
        return self.num_devices

    def get_num_buffer_devices(self):
        return self.num_buffer_devices

    def get_total_num_devices(self):
        return self.num_devices + self.num_buffer_devices

    def get_device_selection_strategy(self):
        return self.device_selection_strategy

    def get_termination_criteria(self):
        return [get_termination_criteria_from_json(
            criteria) for criteria in self.termination_criteria]

    def add_termination_criteria(self, termination_criteria):
        """
        :param termination_criteria: TerminationCriteria
        """
        self.termination_criteria.append(termination_criteria.to_json())

    def set_termination_criteria(self, termination_criteria):
        """
        :param termination_criteria: list(TerminationCriteria)
        """
        self.termination_criteria = []
        for criteria in termination_criteria:
            self.termination_criteria.append(criteria.to_json())

    def reset_termination_criteria(self):
        termination_criteria = self.get_termination_criteria()
        updated_criteria = []
        for criteria in termination_criteria:
            criteria.reset()

            updated_criteria.append(criteria.to_json())

        self.termination_criteria = updated_criteria

    def to_json(self):
        return {
            "num_devices": str(self.num_devices),
            "num_buffer_devices": str(self.num_buffer_devices),
            "device_selection_strategy": self.device_selection_strategy,
            "termination_criteria": self.termination_criteria
        }

    @staticmethod
    def from_json(json_data):
        return JobConfiguration(int(json_data["num_devices"]),
                                int(json_data["num_buffer_devices"]),
                                json_data["device_selection_strategy"],
                                json_data["termination_criteria"])
