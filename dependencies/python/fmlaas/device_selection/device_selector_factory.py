from ..model import DeviceSelectionStrategy
from .device_selector import DeviceSelector
from .random_device_selector import RandomDeviceSelector


class DeviceSelectorFactory:

    def get_device_selector(self, selector_name: DeviceSelectionStrategy) -> DeviceSelector:
        if selector_name == DeviceSelectionStrategy.RANDOM:
            return RandomDeviceSelector()

        raise ValueError("device selector name unknown")
