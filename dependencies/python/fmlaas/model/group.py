from .device_builder import DeviceBuilder
from .job_builder import JobBuilder
from .job_status import JobStatus
from .job import Job
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
                 job_info,
                 job_paths,
                 current_job_ids,
                 members,
                 billing):
        """
        :param name: string
        :param id: string
        :param devices: dict
        :param job_info: dict
        :param job_paths: list(list(string))
        :param current_job_ids: list(string)
        :param members: dict
        :param billing: dict
        """
        self.id = id
        self.name = name
        self.devices = devices
        self.job_info = job_info
        self.job_paths = job_paths
        self.current_job_ids = current_job_ids
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

    def add_job_to_path_prev_id(self, prev_job_id, job_id):
        """
        Add a job to a path using the last job ID of that path.

        :param previous_job_id: string
        :param job_id: string
        """
        for path_idx in range(len(self.job_paths)):
            if self.job_paths[path_idx][-1] == prev_job_id:
                self.job_paths[path_idx].append(job_id)
                self._add_job_info(job_id)

                return

    def create_job_path(self, job_id):
        """
        :param job_id: string
        """
        if self.contains_job(job_id):
            return

        self.job_paths.append([job_id])
        self._add_job_info(job_id)

    def _add_job_info(self, job_id):
        """
        :param job_id: string
        """
        self.job_info[job_id] = {}

    def add_current_job_id(self, job_id):
        """
        Adds a job ID to active jobs.

        :param job_id: string
        """
        self.current_job_ids.append(job_id)

    def remove_current_job_id(self, job_id):
        """
        Remove a job ID from active jobs.

        :param job_id: string
        """
        self.current_job_ids.remove(job_id)

    def contains_job(self, job_id):
        """
        :param job_id: string
        :return: boolean
        """
        return job_id in self.job_info

    def get_next_job_in_sequence(self, job_id):
        """
        :param job_id: string
        """
        for job_path in self.job_paths:
            for idx in range(0, len(job_path) - 1):
                if job_path[idx] == job_id:
                    return job_path[idx + 1]

        return None

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_devices(self):
        return self.devices

    def get_device_list(self):
        return list(self.devices.keys())

    def get_current_job_ids(self):
        return self.current_job_ids

    def get_job_paths(self):
        return self.job_paths

    def get_job_info(self):
        return self.job_info

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
            "job_info" : self.job_info,
            "job_paths" : self.job_paths,
            "current_job_ids" : self.current_job_ids,
            "members" : self.members,
            "billing" : self.billing
        }

    @staticmethod
    def from_json(json_data):
        return FLGroup(json_data["name"],
            json_data["ID"],
            json_data["devices"],
            json_data["job_info"],
            json_data["job_paths"],
            json_data["current_job_ids"],
            json_data["members"],
            json_data["billing"])
