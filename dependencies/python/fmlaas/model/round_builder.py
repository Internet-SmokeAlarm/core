from .round import Round
from .round_status import RoundStatus
from .round_configuration import RoundConfiguration
from .builder import Builder

from ..utils.time import get_epoch_time

class RoundBuilder(Builder):

    def __init__(self):
        self.id = None
        self.devices = []
        self.status = RoundStatus.IN_PROGRESS.value
        self.previous_round_id = "N/A"
        self.aggregate_model = {}
        self.start_model = None
        self.end_model = None
        self.configuration = None
        self.models = {}
        self.created_on = get_epoch_time()

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

    def set_previous_round_id(self, previous_round_id):
        """
        :param previous_round_id: string
        """
        self.previous_round_id = previous_round_id

    def set_aggregate_model(self, aggregate_model):
        """
        :param aggregate_model: dict
        """
        self.aggregate_model = aggregate_model

    def set_end_model(self, end_model):
        """
        :param end_model: dict
        """
        self.end_model = end_model

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

    def build(self):
        self._validate_parameters()

        return Round(self.id,
            self.devices,
            self.status,
            self.previous_round_id,
            self.aggregate_model,
            self.start_model,
            self.end_model,
            self.configuration,
            self.models,
            self.created_on)

    def _validate_parameters(self):
        if self.start_model is None:
            raise ValueError("Start model must not be none")
        elif type(self.start_model) is not type({}):
            raise ValueError("Start model must be type dict")

        if self.id is None:
            raise ValueError("ID must not be none")
        elif type(self.id) is not type("str"):
            raise ValueError("ID must be type string")

        if self.configuration is None:
            raise ValueError("configuration must not be none")
        elif type(self.configuration) is not type({}):
            raise ValueError("configuration must be type dict")
