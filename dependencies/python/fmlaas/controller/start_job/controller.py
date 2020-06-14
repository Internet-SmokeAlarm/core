from ...database import DB
from ...model import DBObject
from ...model import JobBuilder
from ...model import Job
from ...model import Project
from ...model import Model
from ...model import ProjectPrivilegeTypesEnum
from ...model import JobConfiguration
from ...device_selection import DeviceSelector
from ...request_processor import AuthContextProcessor
from ...exception import raise_default_request_forbidden_error
from ... import generate_unique_id
from ..utils.auth.conditions import IsUser
from ..utils.auth.conditions import HasProjectPermissions
from ..utils.auth.conditions import ProjectContainsExperiment
from ...device_selection import DeviceSelectorFactory
from ..abstract_controller import AbstractController


class StartJobController(AbstractController):

    def __init__(self,
                 job_db: DB,
                 project_db: DB,
                 project_id: str,
                 experiment_id: str,
                 job_config: JobConfiguration,
                 auth_context: AuthContextProcessor):
        super(StartJobController, self).__init__(auth_context)

        self.job_db = job_db
        self.project_db = project_db
        self.project_id = project_id
        self.experiment_id = experiment_id
        self.job_config = job_config

    def load_data(self):
        self.project = DBObject.load_from_db(Project, self.project_id, self.project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self.project, ProjectPrivilegeTypesEnum.READ_WRITE),
                ProjectContainsExperiment(self.project, self.experiment_id)
            ]
        ]

    def execute_controller(self):
        experiment = self.project.get_experiment(self.experiment_id)
        project_device_list = self.project.get_device_list()
        if self.job_config.get_num_devices() > len(project_device_list):
            raise ValueError(
                "Cannot start job with more devices than exist in project.")

        device_selector = self.get_device_selector()
        devices = device_selector.select_devices(project_device_list, self.job_config)

        new_job = self.create_job(devices)

        if not experiment.is_active:
            new_job.set_start_model(experiment.current_model)

        experiment.add_job(new_job)
        self.project.add_or_update_experiment(experiment)

        new_job.save_to_db(self.job_db)
        self.project.save_to_db(self.project_db)

        return new_job.get_id()

    def get_device_selector(self) -> DeviceSelector:
        return DeviceSelectorFactory().get_device_selector(
            self.job_config.get_device_selection_strategy())

    def create_job(self, devices: list) -> Job:
        builder = JobBuilder()
        builder.set_id(generate_unique_id())
        builder.set_project_id(self.project_id)
        builder.set_experiment_id(self.experiment_id)
        builder.set_configuration(self.job_config.to_json())
        builder.set_devices(devices)

        return builder.build()
