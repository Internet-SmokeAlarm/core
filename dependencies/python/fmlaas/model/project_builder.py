from .project import Project
from .builder import Builder


class ProjectBuilder(Builder):

    def __init__(self):
        self.name = None
        self._description = ""
        self.id = None
        self.devices = {}
        self.experiments = {}
        self.members = {}
        self.billing = {}

    def set_description(self, description: str) -> None:
        self._description = description

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

    def set_experiments(self, experiments):
        """
        :param experiments: dict
        """
        self.experiments = experiments

    def set_billing(self, billing):
        """
        :param billing: dict
        """
        self.billing = billing

    def build(self):
        self._validate_parameters()

        return Project(self.name,
                       self.id,
                       self.devices,
                       self.experiments,
                       self.members,
                       self.billing,
                       description=self._description)

    def _validate_parameters(self):
        if self.id is None:
            raise ValueError("ID must not be none")
        elif not isinstance(self.id, type("str")):
            raise ValueError("ID must be type string")

        if self.name is None:
            raise ValueError("name must not be none")
        elif not isinstance(self.name, type("str")):
            raise ValueError("name must be type string")
