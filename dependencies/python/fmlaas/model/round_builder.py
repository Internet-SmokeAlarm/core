from .round import Round
from .round_status import RoundStatus
from .round_configuration import RoundConfiguration

from ..utils.time import get_epoch_time

class RoundBuilder:

    def __init__(self):
        self.id = None
        self.devices = []
        self.status = RoundStatus.IN_PROGRESS
        self.previous_round_id = "N/A"
        self.aggregate_model = {}
        self.configuration = None
        self.models = {}
        self.created_on = get_epoch_time()

    def set_id(self, id):
        self.id = id

    def set_devices(self, devices):
        self.devices = devices

    def set_previous_round_id(self, previous_round_id):
        self.previous_round_id = previous_round_id

    def set_aggregate_model(self, aggregate_model):
        self.aggregate_model = aggregate_model

    def set_configuration(self, configuration):
        self.configuration = configuration

    def set_models(self, models):
        self.models = models

    def build(self):
        self._validate_parameters()

        return Round(self.id,
            self.devices,
            self.status,
            self.previous_round_id,
            self.aggregate_model,
            self.configuration,
            self.models,
            self.created_on)

    def _validate_parameters(self):
        if self.id is None:
            raise ValueError("ID must not be none")
        elif type(self.id) is not type("str"):
            raise ValueError("ID must be type string")

        if self.configuration is None:
            raise ValueError("configuration must not be none")
        elif type(self.configuration) is not type({}):
            raise ValueError("configuration must be type dict")
