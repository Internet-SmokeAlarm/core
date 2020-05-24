from .project import Project
from .builder import Builder

class ProjectBuilder(Builder):

    def __init__(self):
        self.name = None
        self.id = None
        self.devices = {}
        self.job_info = {}
        self.job_paths = []
        self.current_job_ids = []
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

    def set_job_info(self, job_info):
        """
        :param jobs: dict
        """
        self.job_info = job_info

    def set_job_paths(self, job_paths):
        """
        :param job_paths: list(list(string))
        """
        self.job_paths = job_paths

    def set_current_job_ids(self, current_job_ids):
        """
        :param current_job_ids: list(string)
        """
        self.current_job_ids = current_job_ids

    def set_billing(self, billing):
        """
        :param billing: dict
        """
        self.billing = billing

    def build(self):
        self._validate_parameters()

        return Project(self.name, self.id, self.devices, self.job_info, self.job_paths, self.current_job_ids, self.members, self.billing)

    def _validate_parameters(self):
        if self.id is None:
            raise ValueError("ID must not be none")
        elif type(self.id) is not type("str"):
            raise ValueError("ID must be type string")

        if self.name is None:
            raise ValueError("name must not be none")
        elif type(self.name) is not type("str"):
            raise ValueError("name must be type string")
