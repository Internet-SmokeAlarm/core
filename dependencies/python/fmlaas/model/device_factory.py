from dependencies.python.fmlaas.model.api_key import ApiKey
from ..utils.time import get_epoch_time
from .device import Device


class DeviceFactory:
    
    @staticmethod
    def create_device(id: str) -> Device:
        registered_at = get_epoch_time()

        return Device(id, registered_at)
