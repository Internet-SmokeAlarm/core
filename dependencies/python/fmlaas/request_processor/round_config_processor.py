from .request_processor import RequestProcessor

class RoundConfigJSONProcessor(RequestProcessor):

    DEVICE_SELECTION_STRATEGY_KEY = "device_selection_strategy"
    NUM_DEVICES_KEY = "num_devices"

    def __init__(self, json):
        self.json = json

    def get_device_selection_strategy(self):
        device_selection_strategy = self.json.get(RoundConfigJSONProcessor.DEVICE_SELECTION_STRATEGY_KEY, None)

        if not self._is_string_name_valid(device_selection_strategy):
            raise ValueError("Device selection strategy invalid.")

        return device_selection_strategy

    def get_num_devices(self):
        num_devices = self.json.get(RoundConfigJSONProcessor.NUM_DEVICES_KEY, None)

        if not self._is_string_name_valid(num_devices):
            raise ValueError("Num devices invalid.")

        return num_devices
