from .project import Project
from .builder import Builder


class ProjectBuilder(Builder):

    def __init__(self):
        self.name = None
        self.id = None
        self.devices = {}
        self.job_sequences = {}
        self.members = {}
        self.billing = {}

    def set_name(self, name):
        """
        :param name: string
        """
        self.name = name

    def set_id(self, id):
        """
        :param id: string
        """
        self.id = id

    def set_devices(self, devices):
        """
        :param devices: dict
        """
        self.devices = devices

    def set_job_sequences(self, job_sequences):
        """
        :param job_sequences: dict
        """
        self.job_sequences = job_sequences

    def set_billing(self, billing):
        """
        :param billing: dict
        """
        self.billing = billing

    def build(self):
        self._validate_parameters()

        return Project(self.name, self.id, self.devices, self.job_sequences, self.members, self.billing)

    def _validate_parameters(self):
        if self.id is None:
            raise ValueError("ID must not be none")
        elif not isinstance(self.id, type("str")):
            raise ValueError("ID must be type string")

        if self.name is None:
            raise ValueError("name must not be none")
        elif not isinstance(self.name, type("str")):
            raise ValueError("name must be type string")
