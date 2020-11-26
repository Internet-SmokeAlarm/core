from abc import abstractmethod
from typing import List

from ..model import JobConfiguration


class DeviceSelector:

    @abstractmethod
    def select_devices(self, devices: List[str], job_config: JobConfiguration) -> List[str]:
        raise NotImplementedError("select_devices() not implemented")
