from .device_builder import DeviceBuilder
from .round_builder import RoundBuilder
from .round_status import RoundStatus
from .round import Round
from ..generate_unique_id import generate_unique_id
from ..device_selection import DeviceSelectorFactory

from .db_object import DBObject

class FLGroup(DBObject):

    def __init__(self, name, id, devices, rounds, current_round_id):
        """
        :param name: string
        :param id: string
        :param devices: dict
        :param rounds: dict
        :param current_round_id: string
        """
        self.id = id
        self.name = name
        self.devices = devices
        self.rounds = rounds
        self.current_round_id = current_round_id

    def add_device(self, device_id):
        """
        :param device_id: string
        """
        builder = DeviceBuilder()
        builder.set_id(device_id)
        device = builder.build()

        self.devices[device_id] = device.to_json()

    def add_round(self, round_id):
        """
        :param round_id: string
        """
        self.rounds[round_id] = True

    def set_current_round_id(self, round_id):
        """
        :param round_id: string
        """
        self.current_round_id = round_id

    def contains_round(self, round_id):
        """
        :param round_id: string
        :return: boolean
        """
        return round_id in self.rounds

    def get_initial_model(self):
        return self.id

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_devices(self):
        return self.devices

    def get_device_list(self):
        return list(self.devices.keys())

    def get_rounds(self):
        return self.rounds

    def get_current_round_id(self):
        return self.current_round_id

    def to_json(self):
        return {
            "name" : self.name,
            "ID" : self.id,
            "devices" : self.devices,
            "rounds" : self.rounds,
            "current_round_id" : self.current_round_id
        }

    @staticmethod
    def from_json(json_data):
        return FLGroup(json_data["name"],
            json_data["ID"],
            json_data["devices"],
            json_data["rounds"],
            json_data["current_round_id"])
