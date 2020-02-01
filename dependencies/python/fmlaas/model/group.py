from .device_builder import DeviceBuilder
from .round_builder import RoundBuilder
from .round_status import RoundStatus
from .round import Round
from .model import Model
from .group_privilege_types import GroupPrivilegeTypesEnum
from ..generate_unique_id import generate_unique_id
from ..device_selection import DeviceSelectorFactory

from .db_object import DBObject

class FLGroup(DBObject):

    def __init__(self, name, id, devices, rounds, current_round_id, initial_model, members):
        """
        :param name: string
        :param id: string
        :param devices: dict
        :param rounds: dict
        :param current_round_id: string
        :param initial_model: dict
        :param members: dict
        """
        self.id = id
        self.name = name
        self.devices = devices
        self.rounds = rounds
        self.current_round_id = current_round_id
        self.initial_model = initial_model
        self.members = members

    def add_device(self, device_id):
        """
        :param device_id: string
        """
        builder = DeviceBuilder()
        builder.set_id(device_id)
        device = builder.build()

        self.devices[device_id] = device.to_json()

    def contains_device(self, device_id):
        """
        :param device_id: string
        """
        return device_id in self.devices

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

    def is_initial_model_set(self):
        """
        :return: boolean
        """
        return Model.is_valid_json(self.initial_model)

    def get_initial_model(self):
        return Model.from_json(self.initial_model)

    def set_initial_model(self, initial_model):
        """
        :param initial_model: Model
        """
        self.initial_model = initial_model.to_json()

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

    def is_member(self, user_id):
        """
        :param user_id: string
        """
        return user_id in self.members

    def add_or_update_member(self, user_id, permission_level):
        """
        :param user_id: string
        :param permission_level: GroupPrivilegeTypesEnum
        """
        self.members[user_id] = {"permission_level" : permission_level.value}

    def get_member_auth_level(self, user_id):
        """
        :param user_id: string
        """
        return GroupPrivilegeTypesEnum(self.members[user_id]["permission_level"])

    def does_member_have_auth(self, user_id, permission_level):
        """
        :param user_id: string
        :param permission_level: GroupPrivilegeTypesEnum
        """
        if not self.is_member(user_id):
            return False
        else:
            return self.get_member_auth_level(user_id).value >= permission_level.value

    def get_members(self):
        return self.members

    def to_json(self):
        return {
            "name" : self.name,
            "ID" : self.id,
            "devices" : self.devices,
            "rounds" : self.rounds,
            "current_round_id" : self.current_round_id,
            "initial_model" : self.initial_model,
            "members" : self.members
        }

    @staticmethod
    def from_json(json_data):
        return FLGroup(json_data["name"],
            json_data["ID"],
            json_data["devices"],
            json_data["rounds"],
            json_data["current_round_id"],
            json_data["initial_model"],
            json_data["members"])
