from .round import Round
from .round_status import RoundStatus
from .round_configuration import RoundConfiguration
from .builder import Builder

from ..utils.time import get_epoch_time

class RoundBuilder(Builder):

    def __init__(self):
        self.id = None
        self.devices = []
        self.status = RoundStatus.INITIALIZED.value
        self.aggregate_model = {}
        self.start_model = {}
        self.configuration = None
        self.models = {}
        self.created_on = get_epoch_time()
        self.billable_size = "0"

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
        self.set_status(RoundStatus.IN_PROGRESS)

    def set_billable_size(self, billable_size):
        """
        :param billable_size: string
        """
        self.billable_size = billable_size

    def set_status(self, status):
        """
        :param status: RoundStatus
        """
        self.status = status.value

    def build(self):
        self._validate_parameters()

        return Round(self.id,
            self.devices,
            self.status,
            self.aggregate_model,
            self.start_model,
            self.configuration,
            self.models,
            self.created_on,
            self.billable_size)

    def _validate_parameters(self):
        if self.id is None:
            raise ValueError("ID must not be none")
        elif type(self.id) is not type("str"):
            raise ValueError("ID must be type string")

        if self.configuration is None:
            raise ValueError("configuration must not be none")
        elif type(self.configuration) is not type({}):
            raise ValueError("configuration must be type dict")
