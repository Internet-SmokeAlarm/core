from typing import Dict, List

from .db_object import DBObject
from .device import Device
from .experiment import Experiment
from .project_privilege_types import ProjectPrivilegeTypesEnum


class Project(DBObject):

    def __init__(self,
                 name: str,
                 id: str,
                 devices: dict,
                 experiments: dict,
                 members: dict,
                 billing: dict,
                 description: str):
        super(Project, self).__init__(id)

        self._name = name
        self._devices = devices
        self._experiments = experiments
        self._members = members
        self._billing = billing
        self._description = description

    @property
    def description(self) -> str:
        return self._description
    
    @property
    def experiments(self) -> List[Experiment]:
        return [self.get_experiment(x) for x in self._experiments.keys()]

    @property
    def name(self) -> str:
        return self._name

    @property
    def devices(self) -> dict:
        return self._devices
    
    @property
    def billing(self) -> dict:
        return self._billing
    
    @property
    def members(self) -> dict:
        return self._members

    def add_device(self, device: Device) -> None:
        self.devices[device.id] = device.to_json()

    def contains_device(self, device_id: str) -> bool:
        return device_id in self.devices

    def add_or_update_experiment(self, experiment: Experiment) -> None:
        self._experiments[experiment.id] = experiment.to_json()

    def get_experiment(self, id: str) -> Experiment:
        return Experiment.from_json(self._experiments[id])

    def contains_experiment(self, experiment_id: str) -> bool:
        return experiment_id in self._experiments

    def contains_job(self, exp_id: str, job_id: str) -> bool:
        return self.get_experiment(exp_id).contains_job(job_id)
    
    def get_num_experiments(self) -> int:
        return len(self._experiments.keys())
    
    def get_next_experiment_id(self) -> str:
        return str(self.get_num_experiments() + 1)

    def get_active_jobs(self) -> List[Dict[str, str]]:
        active_jobs = []
        for i in self._experiments.keys():
            experiment = self.get_experiment(i)
            if experiment.current_job and experiment.current_job.is_in_progress():
                active_jobs.append({
                    "experiment_id": experiment.id,
                    "job_id": experiment.current_job.id
                })

        return active_jobs
    
    def get_active_jobs_for_device(self, device_id: str) -> List[Dict[str, str]]:
        active_jobs = []
        for i in self._experiments.keys():
            experiment = self.get_experiment(i)
            if experiment.current_job and experiment.current_job.is_in_progress() and experiment.current_job.contains_device(device_id):
                active_jobs.append({
                    "experiment_id": experiment.id,
                    "job_id": experiment.current_job.id
                })

        return active_jobs
    
    def get_device_list(self) -> List[str]:
        return list(self._devices.keys())

    def is_member(self, user_id: str) -> bool:
        return user_id in self._members

    def add_or_update_member(self,
                             user_id: str,
                             permission_level: ProjectPrivilegeTypesEnum) -> None:
        self._members[user_id] = {"permission_level": str(permission_level.value)}

    def get_member_auth_level(self, user_id: str) -> ProjectPrivilegeTypesEnum:
        return ProjectPrivilegeTypesEnum(int(self._members[user_id]["permission_level"]))

    def does_member_have_auth(self,
                              user_id: str,
                              permission_level: ProjectPrivilegeTypesEnum) -> bool:
        if self.is_member(user_id):
            return self.get_member_auth_level(
                user_id).value >= permission_level.value
        else:
            return False

    def get_all_job_ids(self) -> List[str]:
        jobs = []
        for experiment in self.experiments:
            jobs.extend(experiment.jobs)

        return jobs

    def to_json(self) -> dict:
        return {
            "name": self._name,
            "ID": self._id,
            "devices": self._devices,
            "experiments": self._experiments,
            "members": self._members,
            "billing": self._billing,
            "description": self._description
        }

    def __eq__(self, other) -> bool:
        return (type(other) == type(self)) and \
            (other._name == self._name) and \
            (self._experiments == other._experiments) and \
            (self._devices == other._devices) and \
            (self._members == other._members) and \
            (self._billing == other._billing) and \
            (self._id == other._id) and \
            (self._description == other._description)

    @staticmethod
    def from_json(json_data):
        return Project(json_data["name"],
                       json_data["ID"],
                       json_data["devices"],
                       json_data["experiments"],
                       json_data["members"],
                       json_data["billing"],
                       json_data["description"])
