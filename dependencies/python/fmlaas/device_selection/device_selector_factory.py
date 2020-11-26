from .device_selector import DeviceSelector
from .random_device_selector import RandomDeviceSelector


class DeviceSelectorFactory:

    def get_device_selector(self, selector_name: str) -> DeviceSelector:
        if selector_name == "RANDOM":
            return RandomDeviceSelector()

        raise ValueError("device selector name unknown")
