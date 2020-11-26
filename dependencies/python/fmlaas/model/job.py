from typing import List

from .job_configuration import JobConfiguration
from .model import Model
from .status import Status
from .testing_report import TestingReport


class Job:

    def __init__(self,
                 id: str,
                 devices: List[str],
                 status: Status,
                 aggregate_model: dict,
                 start_model: dict,
                 configuration: JobConfiguration,
                 models: dict,
                 created_at: int,
                 billable_size: int,
                 testing_reports: dict):
        self._id = id
        self._devices = devices
        self._status = status
        self._aggregate_model = aggregate_model
        self._start_model = start_model
        self._configuration = configuration
        self._models = models
        self._created_at = created_at
        self._billable_size = billable_size
        self._testing_reports = testing_reports

    @property
    def id(self) -> str:
        return self._id

    @property
    def devices(self) -> List[str]:
        return self._devices

    @property
    def status(self) -> Status:
        return self._status
    
    @status.setter
    def status(self, status: Status) -> None:
        self._status = status

    @property
    def aggregate_model(self) -> Model:
        return Model.from_json(self._aggregate_model)
    
    @aggregate_model.setter
    def aggregate_model(self, aggregate_model: Model) -> None:
        self._aggregate_model = aggregate_model.to_json()

    @property
    def start_model(self) -> Model:
        return Model.from_json(self._start_model)

    @start_model.setter
    def start_model(self, start_model: Model) -> None:
        if not self.is_in_initialization():
            return

        self._start_model = start_model.to_json()
        self._status = Status.IN_PROGRESS

    @property
    def end_model(self) -> Model:
        if self.is_aggregate_model_set():
            return self.aggregate_model
        else:
            return self.start_model

    @property
    def testing_reports(self) -> dict:
        return self._testing_reports

    @property
    def configuration(self) -> JobConfiguration:
        return self._configuration
    
    @configuration.setter
    def configuration(self, config: JobConfiguration) -> None:
        self._configuration = config

    @property
    def models(self) -> dict:
        model_objs = {}
        for model in list(self._models.keys()):
            model_objs[model] = Model.from_json(self._models[model])

        return model_objs

    @property
    def created_at(self) -> int:
        return self._created_at
    
    @property
    def billable_size(self) -> int:
        return self._billable_size
    
    @billable_size.setter
    def billable_size(self, billable_size: int) -> None:
        self._billable_size = billable_size

    def add_model(self, model: Model) -> None:
        self._models[model.entity_id] = model.to_json()

    def should_aggregate(self) -> bool:
        return self.is_ready_for_aggregation() and self.is_in_progress()

    def is_ready_for_aggregation(self) -> bool:
        return len(list(self._models.keys())) >= self._configuration.num_devices

    def is_aggregate_model_set(self) -> bool:
        return Model.is_valid_json(self._aggregate_model)

    def is_start_model_set(self) -> bool:
        return Model.is_valid_json(self._start_model)

    def is_complete(self) -> bool:
        return self._status == Status.COMPLETED

    def is_active(self) -> bool:
        return self.is_in_progress() or self.is_aggregation_in_progress()

    def is_in_initialization(self) -> bool:
        return self._status == Status.INITIALIZED

    def is_in_progress(self) -> bool:
        return self._status == Status.IN_PROGRESS

    def is_aggregation_in_progress(self) -> bool:
        return self._status == Status.AGGREGATION_IN_PROGRESS

    def is_cancelled(self) -> bool:
        return self._status == Status.CANCELLED

    def contains_device(self, device_id: str) -> bool:
        return device_id in self._devices

    def is_device_model_submitted(self, device_id: str) -> bool:
        return device_id in self._models

    def is_device_active(self, device_id: str) -> bool:
        if self.is_active() and self.contains_device(device_id):
            return not self.is_device_model_submitted(device_id)

        return False

    def cancel(self) -> None:
        self._status = Status.CANCELLED
        self._end_model = self._start_model

        self._billable_size = self.calculate_billable_size()

    def complete(self) -> None:
        self._status = Status.COMPLETED
        self._end_model = self._aggregate_model

        self._billable_size = self.calculate_billable_size()

    def calculate_billable_size(self) -> int:
        """
        Calculates the billable size of the data stored in this job.
        """
        billable_size = 0

        for device_id, model in self._models.items():
            billable_size += int(model["size"])

        if self.is_aggregate_model_set():
            billable_size += self.aggregate_model.size

        if self.is_start_model_set():
            billable_size += self.start_model.size

        return billable_size

    def should_terminate(self) -> bool:
        """
        Returns True if the job should be terminated, false if not. "should be" is determined
        by termination criteria in job configuration.
        """
        termination_criteria = self._configuration.termination_criteria
        for criteria in termination_criteria:
            if criteria.is_criteria_satisfied():
                return True

        return False

    def reset_termination_criteria(self) -> None:
        self._configuration.reset_termination_criteria()

    def add_testing_report(self, testing_report: TestingReport) -> None:
        self._testing_reports[testing_report.device_id] = testing_report.to_json()

    def to_json(self) -> dict:
        return {
            "ID": self._id,
            "status": self._status.value,
            "devices": self._devices,
            "aggregate_model": self._aggregate_model,
            "start_model": self._start_model,
            "configuration": self._configuration.to_json(),
            "models": self._models,
            "created_at": str(self._created_at),
            "billable_size": str(self._billable_size),
            "testing_reports": self._testing_reports
        }

    def __eq__(self, other) -> bool:
        return (type(other) == type(self)) and \
            (self._id == other._id) and \
            (self._status == other._status) and \
            (self._devices == other._devices) and \
            (self._aggregate_model == other._aggregate_model) and \
            (self._start_model == other._start_model) and \
            (self._configuration == other._configuration) and \
            (self._models == other._models) and \
            (self._created_at == other._created_at) and \
            (self._billable_size == other._billable_size) and \
            (self._testing_reports == other._testing_reports)

    @staticmethod
    def from_json(json_data):
        return Job(json_data["ID"],
                   json_data["devices"],
                   Status(json_data["status"]),
                   json_data["aggregate_model"],
                   json_data["start_model"],
                   JobConfiguration.from_json(json_data["configuration"]),
                   json_data["models"],
                   int(json_data["created_at"]),
                   int(json_data["billable_size"]),
                   json_data["testing_reports"])
