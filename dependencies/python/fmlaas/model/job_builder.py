from .job import Job
from .job_status import JobStatus
from .job_configuration import JobConfiguration
from .builder import Builder

from ..utils.time import get_epoch_time


class JobBuilder(Builder):

    def __init__(self):
        self.id = None
        self.devices = []
        self.status = JobStatus.INITIALIZED.value
        self.aggregate_model = {}
        self.start_model = {}
        self.configuration = None
        self.models = {}
        self.created_on = get_epoch_time()
        self.billable_size = "0"
        self.project_id = None
        self.job_sequence_id = None

    def set_id(self, id):
        """
        :param id: string
        """
        self.id = id

    def set_devices(self, devices):
        """
        :param devices: list(string)
        """
        self.devices = devices

    def set_aggregate_model(self, aggregate_model):
        """
        :param aggregate_model: dict
        """
        self.aggregate_model = aggregate_model

    def set_configuration(self, configuration):
        """
        :param configuration: dict
        """
        self.configuration = configuration

    def set_models(self, models):
        """
        :param models: dict
        """
        self.models = models

    def set_start_model(self, start_model):
        """
        :param start_model: dict
        """
        self.start_model = start_model
        self.set_status(JobStatus.IN_PROGRESS)

    def set_billable_size(self, billable_size):
        """
        :param billable_size: string
        """
        self.billable_size = billable_size

    def set_status(self, status):
        """
        :param status: JobStatus
        """
        self.status = status.value

    def set_project_id(self, project_id):
        """
        :param project_id: string
        """
        self.project_id = project_id

    def set_job_sequence_id(self, job_sequence_id):
        """
        :param job_sequence_id: string
        """
        self.job_sequence_id = job_sequence_id

    def build(self):
        self._validate_parameters()

        return Job(self.id,
                   self.devices,
                   self.status,
                   self.aggregate_model,
                   self.start_model,
                   self.configuration,
                   self.models,
                   self.created_on,
                   self.billable_size,
                   self.project_id,
                   self.job_sequence_id)

    def _validate_parameters(self):
        if self.id is None:
            raise ValueError("ID must not be none")
        elif not isinstance(self.id, type("str")):
            raise ValueError("ID must be type string")

        if self.configuration is None:
            raise ValueError("configuration must not be none")
        elif not isinstance(self.configuration, type({})):
            raise ValueError("configuration must be type dict")

        if self.project_id is None:
            raise ValueError("Parent Project ID must not be none")
        elif not isinstance(self.project_id, type("str")):
            raise ValueError("Parent Project ID must be type string")

        if self.job_sequence_id is None:
            raise ValueError("Parent Job Sequence ID must not be none")
        elif not isinstance(self.job_sequence_id, type("str")):
            raise ValueError("Parent Job Sequence ID must be type string")
