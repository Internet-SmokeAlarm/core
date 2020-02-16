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

    def __init__(self,
                 name,
                 id,
                 devices,
                 round_info,
                 round_paths,
                 current_round_ids,
                 members,
                 billing):
        """
        :param name: string
        :param id: string
        :param devices: dict
        :param round_info: dict
        :param round_paths: list(list(string))
        :param current_round_ids: list(string)
        :param members: dict
        :param billing: dict
        """
        self.id = id
        self.name = name
        self.devices = devices
        self.round_info = round_info
        self.round_paths = round_paths
        self.current_round_ids = current_round_ids
        self.members = members
        self.billing = billing

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

    def add_round_to_path_prev_id(self, prev_round_id, round_id):
        """
        Add a round to a path using the last round ID of that path.

        :param previous_round_id: string
        :param round_id: string
        """
        for path_idx in range(len(self.round_paths)):
            if self.round_paths[path_idx][-1] == prev_round_id:
                self.round_paths[path_idx].append(round_id)
                self._add_round_info(round_id)

                return

    def create_round_path(self, round_id):
        """
        :param round_id: string
        """
        if self.contains_round(round_id):
            return

        self.round_paths.append([round_id])
        self._add_round_info(round_id)

    def _add_round_info(self, round_id):
        """
        :param round_id: string
        """
        self.round_info[round_id] = {}

    def add_current_round_id(self, round_id):
        """
        Adds a round ID to active rounds.

        :param round_id: string
        """
        self.current_round_ids.append(round_id)

    def remove_current_round_id(self, round_id):
        """
        Remove a round ID from active rounds.

        :param round_id: string
        """
        self.current_round_ids.remove(round_id)

    def contains_round(self, round_id):
        """
        :param round_id: string
        :return: boolean
        """
        return round_id in self.round_info

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

    def get_current_round_ids(self):
        return self.current_round_ids

    def get_round_paths(self):
        return self.round_paths

    def get_round_info(self):
        return self.round_info

    def get_billing(self):
        return self.billing

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
            "round_info" : self.round_info,
            "round_paths" : self.round_paths,
            "current_round_ids" : self.current_round_ids,
            "members" : self.members,
            "billing" : self.billing
        }

    @staticmethod
    def from_json(json_data):
        return FLGroup(json_data["name"],
            json_data["ID"],
            json_data["devices"],
            json_data["round_info"],
            json_data["round_paths"],
            json_data["current_round_ids"],
            json_data["members"],
            json_data["billing"])
