from ...database import DB
from ...device_selection import DeviceSelector, DeviceSelectorFactory
from ...model import (DBObject, Job, JobConfiguration, JobFactory, Project,
                      ProjectPrivilegeTypesEnum)
from ...request_processor import AuthContextProcessor
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import HasProjectPermissions, IsUser


class StartJobController(AbstractController):

    def __init__(self,
                 project_db: DB,
                 project_id: str,
                 experiment_id: str,
                 job_config: JobConfiguration,
                 auth_context: AuthContextProcessor):
        super(StartJobController, self).__init__(auth_context)

        self._project_db = project_db
        self._project_id = project_id
        self._experiment_id = experiment_id
        self._job_config = job_config

        self._project = DBObject.load_from_db(Project, self._project_id, self._project_db)

    def get_auth_conditions(self):
        return [
            [
                IsUser(),
                HasProjectPermissions(self._project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

    def execute_controller(self) -> Job:
        experiment = self._project.get_experiment(self._experiment_id)

        experiment.handle_termination_check()

        project_device_list = self._project.get_device_list()

        if self._job_config.num_devices > len(project_device_list):
            raise ValueError(
                "Cannot start job with more devices than exist in project.")

        device_selector = self.get_device_selector()
        devices = device_selector.select_devices(project_device_list, self._job_config)

        new_job = JobFactory.create_job(experiment.get_next_job_id(),
                                        self._job_config,
                                        devices)

        experiment.add_or_update_job(new_job)

        self._project.add_or_update_experiment(experiment)
        self._project.save_to_db(self._project_db)

        return new_job

    def get_device_selector(self) -> DeviceSelector:
        return DeviceSelectorFactory().get_device_selector(
            self._job_config.device_selection_strategy)
