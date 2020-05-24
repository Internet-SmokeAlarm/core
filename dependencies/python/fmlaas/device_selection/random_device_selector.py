import random

from .device_selector import DeviceSelector


class RandomDeviceSelector(DeviceSelector):

    def select_devices(self, devices, round_configuration):
        return random.sample(devices, int(
            round_configuration.get_total_num_devices()))
