from .round_status import RoundStatus
from .round_configuration import RoundConfiguration
from .model import Model

from .db_object import DBObject

class Round(DBObject):

    def __init__(self,
                 id,
                 devices,
                 status,
                 previous_round_id,
                 aggregate_model,
                 start_model,
                 end_model,
                 configuration,
                 models,
                 created_on):
        """
        :param id: string
        :param devices: list(string)
        :param status: string
        :param previous_round_id: string
        :param aggregate_model: dict
        :param start_model: dict
        :param end_model: dict
        :param configuration: dict
        :param models: dict
        :param created_on: string
        """
        self.id = id
        self.devices = devices
        self.status = status
        self.previous_round_id = previous_round_id
        self.aggregate_model = aggregate_model
        self.start_model = start_model
        self.end_model = end_model
        self.configuration = configuration
        self.models = models
        self.created_on = created_on

    def get_id(self):
        return self.id

    def get_devices(self):
        return self.devices

    def get_status(self):
        return RoundStatus(self.status)

    def get_previous_round_id(self):
        return self.previous_round_id

    def get_aggregate_model(self):
        return Model.from_json(self.aggregate_model)

    def get_start_model(self):
        return Model.from_json(self.start_model)

    def get_end_model(self):
        return Model.from_json(self.end_model)

    def get_configuration(self):
        return RoundConfiguration.from_json(self.configuration)

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

    def should_aggregate(self):
        """
        :return: boolean
        """
        return self.is_ready_for_aggregation() and self.is_in_progress()

    def is_ready_for_aggregation(self):
        """
        :return: boolean
        """
        return len(self.devices) == len(list(self.models.keys()))

    def is_aggregate_model_set(self):
        """
        :return: boolean
        """
        return Model.is_valid_json(self.aggregate_model)

    def set_aggregate_model(self, aggregate_model):
        """
        :param aggregate_model: Model
        """
        self.aggregate_model = aggregate_model.to_json()

    def is_complete(self):
        """
        :return: boolean
        """
        return self.get_status() == RoundStatus.COMPLETED

    def is_active(self):
        """
        :return: boolean
        """
        return self.is_in_progress() or self.is_aggregation_in_progress()

    def is_in_progress(self):
        """
        :return: boolean
        """
        return self.get_status() == RoundStatus.IN_PROGRESS

    def is_aggregation_in_progress(self):
        """
        :return: boolean
        """
        return self.get_status() == RoundStatus.AGGREGATION_IN_PROGRESS

    def is_cancelled(self):
        """
        :return: boolean
        """
        return self.get_status() == RoundStatus.CANCELLED

    def contains_device(self, device_id):
        """
        :param device_id: string
        :return: boolean
        """
        return device_id in self.devices

    def is_device_model_submitted(self, device_id):
        """
        :param device_id: string
        :return: boolean
        """
        return device_id in self.models

    def is_device_active(self, device_id):
        """
        :param device_id: string
        :return: boolean
        """
        if self.is_active() and self.contains_device(device_id):
            return not self.is_device_model_submitted(device_id)

        return False

    def set_status(self, status):
        """
        :param status: RoundStatus
        """
        self.status = status.value

    def cancel(self):
        """
        Cancels this round
        """
        self.set_status(RoundStatus.CANCELLED)
        self.end_model = self.start_model

    def complete(self):
        """
        Completes the round
        """
        self.set_status(RoundStatus.COMPLETED)
        self.end_model = self.aggregate_model

    def to_json(self):
        return {
            "ID" : self.id,
            "status" : self.status,
            "devices" : self.devices,
            "previous_round_id" : self.previous_round_id,
            "aggregate_model" : self.aggregate_model,
            "start_model" : self.start_model,
            "end_model" : self.end_model,
            "configuration" : self.configuration,
            "models" : self.models,
            "created_on" : self.created_on
        }

    @staticmethod
    def from_json(json_data):
        return Round(json_data["ID"],
            json_data["devices"],
            json_data["status"],
            json_data["previous_round_id"],
            json_data["aggregate_model"],
            json_data["start_model"],
            json_data["end_model"],
            json_data["configuration"],
            json_data["models"],
            json_data["created_on"])
