from .device_builder import DeviceBuilder
from .job_builder import JobBuilder
from .job_status import JobStatus
from .experiment import Experiment
from .job import Job
from .model import Model
from .project_privilege_types import ProjectPrivilegeTypesEnum
from ..generate_unique_id import generate_unique_id
from ..device_selection import DeviceSelectorFactory
from .db_object import DBObject


class Project(DBObject):

    def __init__(self,
                 name,
                 id,
                 devices,
                 experiments,
                 members,
                 billing):
        """
        :param name: string
        :param id: string
        :param devices: dict
        :param experiments: dict
        :param members: dict
        :param billing: dict
        """
        self.id = id
        self.name = name
        self.devices = devices
        self.experiments = experiments
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

    def add_or_update_experiment(self, experiment):
        """
        :param experiment: Experiment
        """
        self.experiments[experiment.id] = experiment.to_json()

    def get_experiment(self, id):
        """
        :param id: string
        """
        return Experiment.from_json(self.experiments[id])

    def get_experiments(self):
        return [self.get_experiment(x) for x in self.experiments.keys()]

    def contains_experiment(self, experiment_id):
        """
        :param experiment_id: string
        """
        return experiment_id in self.experiments

    def contains_job(self, job_id):
        """
        :param id: string
        """
        for i in self.experiments.keys():
            if self.get_experiment(i).contains_job(job_id):
                return True

        return False

    def get_active_jobs(self):
        active_jobs = []
        for i in self.experiments.keys():
            experiment = self.get_experiment(i)
            if experiment.is_active:
                active_jobs.append(experiment.current_job)

        return active_jobs

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
        :param permission_level: ProjectPrivilegeTypesEnum
        """
        self.members[user_id] = {"permission_level": permission_level.value}

    def get_member_auth_level(self, user_id):
        """
        :param user_id: string
        """
        return ProjectPrivilegeTypesEnum(
            self.members[user_id]["permission_level"])

    def does_member_have_auth(self, user_id, permission_level):
        """
        :param user_id: string
        :param permission_level: ProjectPrivilegeTypesEnum
        """
        if not self.is_member(user_id):
            return False
        else:
            return self.get_member_auth_level(
                user_id).value >= permission_level.value

    def get_members(self):
        return self.members

    def get_all_job_ids(self):
        """
        :param project: Project
        """
        jobs = []
        for experiment in self.get_experiments():
            jobs.extend(experiment.jobs)

        return jobs

    def to_json(self):
        return {
            "name": self.name,
            "ID": self.id,
            "devices": self.devices,
            "experiments": self.experiments,
            "members": self.members,
            "billing": self.billing
        }

    def __eq__(self, other):
        return (other.name == self.name) and (self.experiments == other.experiments) and (self.devices == other.devices) and (self.members == other.members) and (self.billing == other.billing) and (self.id == other.id)

    @staticmethod
    def from_json(json_data):
        return Project(json_data["name"],
                       json_data["ID"],
                       json_data["devices"],
                       json_data["experiments"],
                       json_data["members"],
                       json_data["billing"])
