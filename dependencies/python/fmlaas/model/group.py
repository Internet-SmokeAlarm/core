from .device_builder import DeviceBuilder
from .round_builder import RoundBuilder
from .round_status import RoundStatus
from .round import Round
from ..generate_unique_id import generate_unique_id
from ..device_selection import DeviceSelectorFactory

class FLGroup:

    def __init__(self, name, id, devices, rounds, current_round_id):
        """
        :param name: string
        :param id: string
        :param devices: dict
        :param rounds: dict
        :param current_round_id: string
        """
        self.id = id
        self.name = name
        self.devices = devices
        self.rounds = rounds
        self.current_round_id = current_round_id

    def add_device(self, device_id):
        """
        :param device_id: string
        """
        builder = DeviceBuilder()
        builder.set_id(device_id)
        device = builder.build()

        self.devices[device_id] = device.to_json()

    def create_round(self, round_configuration):
        """
        :param round_configuration: RoundConfiguration
        :return: string
        """
        round_id = generate_unique_id()

        device_selector = self.get_device_selector(round_configuration)
        devices = device_selector.select_devices(self.get_device_list(), round_configuration)

        round_builder = RoundBuilder()
        round_builder.set_id(round_id)
        round_builder.set_previous_round_id(self.current_round_id)
        round_builder.set_configuration(round_configuration.to_json())
        round_builder.set_devices(devices)
        round = round_builder.build()

        self.add_round(round)
        self.set_current_round(round.get_id())

        return round_id

    def add_round(self, round):
        """
        :param round: Round
        """
        self.rounds[round.get_id()] = round.to_json()

    def set_current_round(self, round_id):
        """
        :param round_id: string
        """
        if self.is_round_active(self.current_round_id):
            self.update_round_status(self.current_round_id, RoundStatus.CANCELLED)

        self.current_round_id = round_id
        self.update_round_status(self.current_round_id, RoundStatus.IN_PROGRESS)

    def update_round_status(self, round_id, status):
        """
        :param round_id: string
        :param status: RoundStatus
        """
        round = self.get_round(round_id)
        round.set_status(status)
        self.rounds[round_id] = round.to_json()

    def get_device_selector(self, round_configuration):
        """
        :param round_configuration: RoundConfiguration
        :return DeviceSelector
        """
        factory = DeviceSelectorFactory()
        return factory.get_device_selector(round_configuration.get_device_selection_strategy())

    def add_model(self, model):
        """
        :param model: Model
        """
        model_name = model.get_name()

        if model_name.is_device_model_update():
            model.set_entity_id(model_name.get_device_id())

            self.add_model_to_round(model_name.get_round_id(), model)
        elif model_name.is_round_aggregate_model():
            model.set_entity_id(model_name.get_round_id())

            self.set_round_aggregate_model(model_name.get_round_id(), model)

    def add_model_to_round(self, round_id, model):
        """
        :param round_id: string
        :param model: Model
        """
        round = Round.from_json(self.rounds[round_id])
        round.add_model(model)

        self.rounds[round_id] = round.to_json()

    def get_round(self, round_id):
        """
        :param round_id: string
        :return: Round
        """
        return Round.from_json(self.rounds[round_id])

    def contains_round(self, round_id):
        """
        :param round_id: string
        :return: boolean
        """
        return round_id in self.rounds

    def is_round_complete(self, round_id):
        """
        :param round_id: string
        """
        return Round.from_json(self.rounds[round_id]).is_complete()

    def get_models(self, round_id):
        """
        :param round_id: string
        """
        return self.get_round(round_id).get_models()

    def set_round_aggregate_model(self, round_id, model):
        """
        :param round_id: string
        :param global_model: string
        """
        round = self.get_round(round_id)
        round.set_aggregate_model(model)

        self.rounds[round_id] = round.to_json()

    def get_round_aggregate_model(self, round_id):
        """
        :param round_id: string
        :return: Model
        """
        return Round(self.rounds[round_id]).get_aggregate_model()

    def is_device_active(self, device_id):
        """
        :param device_id: string
        :return: boolean
        """
        if self.is_round_active(self.current_round_id):
            round = Round.from_json(self.rounds[self.current_round_id])

            return round.contains_device(device_id)

        return False

    def is_round_active(self, round_id):
        """
        :param round_id: string
        :return: boolean
        """
        if round_id in self.rounds:
            round = Round.from_json(self.rounds[round_id])

            return round.is_active()

        return False

    def get_initial_model(self):
        return self.id

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_devices(self):
        return self.devices

    def get_device_list(self):
        return list(self.devices.keys())

    def get_rounds(self):
        return self.rounds

    def get_current_round_id(self):
        return self.current_round_id

    def to_json(self):
        return {
            "name" : self.name,
            "ID" : self.id,
            "devices" : self.devices,
            "rounds" : self.rounds,
            "current_round_id" : self.current_round_id
        }

    def save_to_db(self, db_):
        """
        :param db_: database
        """
        return db_.create_or_update_object(self.get_id(), self.to_json())

    @staticmethod
    def load_from_db(id, db_):
        """
        Load a specific instance from the DB.

        :param id: int
        :param db_: database
        """
        object = db_.get_object(id)

        return FLGroup.from_json(object)

    @staticmethod
    def from_json(json_data):
        return FLGroup(json_data["name"],
            json_data["ID"],
            json_data["devices"],
            json_data["rounds"],
            json_data["current_round_id"])
