class RoundConfigJSONProcessor:

    DEVICE_SELECTOR_KEY = "device_selection_strategy"
    NUM_DEVICES_KEY = "num_devices"

    def __init__(self, json):
        self.json = json

    def get_device_selector(self):
        device_selector = self.json.get(RoundConfigJSONProcessor.DEVICE_SELECTOR_KEY, None)

        if not self._is_string_name_valid(device_selector):
            raise ValueError("Device selector invalid.")

        return device_selector

    def get_num_devices(self):
        num_devices = self.json.get(RoundConfigJSONProcessor.NUM_DEVICES_KEY, None)

        if not self._is_string_name_valid(num_devices):
            raise ValueError("Num devices invalid.")

        return num_devices
