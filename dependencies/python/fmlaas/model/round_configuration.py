class RoundConfiguration:

    def __init__(self, num_devices, device_selection_strategy):
        """
        :param num_devices: string
        :param device_selection_strategy: string
        """
        self.num_devices = num_devices
        self.device_selection_strategy = device_selection_strategy

    def get_num_devices(self):
        return self.num_devices

    def get_device_selection_strategy(self):
        return self.device_selection_strategy

    def to_json(self):
        return {
            "num_devices" : self.num_devices,
            "device_selection_strategy" : self.device_selection_strategy
        }

    @staticmethod
    def from_json(json_data):
        return RoundConfiguration(json_data["num_devices"], json_data["device_selection_strategy"])
