from .device import Device

from ..utils.time import get_epoch_time

class DeviceBuilder:

    def __init__(self):
        self.id = None
        self.registered_on = get_epoch_time()

    def set_id(self, id):
        """
        :param id: string
        """
        self.id = id

    def build(self):
        self._validate_parameters()

        return Device(self.id, self.registered_on)

    def _validate_parameters(self):
        if self.id == None:
            raise ValueError("ID must not be None")
        elif type(self.id) is not type("str"):
            raise ValueError("ID must be of type string")
