import random
from typing import List

from ..model import JobConfiguration
from .device_selector import DeviceSelector


class RandomDeviceSelector(DeviceSelector):

    def select_devices(self, devices: List[str], job_config: JobConfiguration) -> List[str]:
        return random.sample(devices, int(
            job_config.get_total_num_devices()))
