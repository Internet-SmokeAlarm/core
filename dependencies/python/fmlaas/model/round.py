from .round_status import RoundStatus
from .model import Model

class Round:

    def __init__(self, id, devices, status, previous_round_id, aggregate_model, configuration, models, created_on):
        """
        :param id: string
        :param devices: list(string)
        :param status: RoundStatus
        :param previous_round_id: string
        :param aggregate_model: dict
        :param models: dict
        :param created_on: string
        """
        self.id = id
        self.devices = devices
        self.status = status
        self.previous_round_id = previous_round_id
        self.aggregate_model = aggregate_model
        self.configuration = configuration
        self.models = models
        self.created_on = created_on

    def get_id(self):
        return self.id

    def get_devices(self):
        return self.devices

    def get_status(self):
        return self.status

    def get_previous_round_id(self):
        return self.previous_round_id

    def get_aggregate_model(self):
        return Model.from_json(self.aggregate_model)

    def get_configuration(self):
        return self.configuration

    def get_models(self):
        model_objs = {}
        for model in list(self.models.keys()):
            model_objs[model] = Model.from_json(self.models[model])

        return model_objs

    def get_created_on(self):
        return self.created_on

    def add_model(self, model):
        """
        :param model: Model
        """
        self.models[model.get_entity_id()] = model.to_json()

    def set_aggregate_model(self, aggregate_model):
        """
        :param aggregate_model: Model
        """
        self.aggregate_model = aggregate_model.to_json()

    def is_complete(self):
        return self.status == RoundStatus.COMPLETED

    def to_json(self):
        return {
            "ID" : self.id,
            "status" : self.status.value,
            "devices" : self.devices,
            "previous_round_id" : self.previous_round_id,
            "aggregate_model" : self.aggregate_model,
            "configuration" : self.configuration,
            "models" : self.models,
            "created_on" : self.created_on
        }

    @staticmethod
    def from_json(json_data):
        return Round(json_data["ID"],
            json_data["devices"],
            RoundStatus(json_data["status"]),
            json_data["previous_round_id"],
            json_data["aggregate_model"],
            json_data["configuration"],
            json_data["models"],
            json_data["created_on"])
