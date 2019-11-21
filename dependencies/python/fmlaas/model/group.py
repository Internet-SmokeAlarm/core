class FLGroup:

    def __init__(self, name, id=None, devices=[], rounds=[]):
        self.id = id
        self.name = name
        self.devices = devices
        self.rounds = rounds

    def add_device(self, device_id, device_api_key):
        """
        :param device_id: int
        :param device_api_key: string
        """
        self.devices.append({
            "id" : device_id,
            "api_key" : device_api_key
        })

    def create_round(self, round_id):
        """
        :param round_id: int
        """
        self.rounds.append({
            "id" : round_id,
            "models" : [],
            "combined_model" : ""
        })

    def add_model_to_round(self, round_id, model):
        """
        :param round_id: int
        :param model: string
        """
        for round in self.rounds:
            if round["id"] == round_id:
                round["models"].append(model)

                return

    def get_round(self, round_id):
        """
        :param round_id: int
        """
        for round in self.rounds:
            if round["id"] == round_id:
                return round

    def get_models(self, round_id):
        """
        :param round_id: int
        """
        round = self.get_round(round_id)

        return round["models"]

    def set_round_global_model(self, round_id, global_model):
        """
        :param round_id: int
        :param global_model: string
        """
        round = self.get_round(round_id)
        round["combined_model"] = global_model

    def get_round_aggregate_model(self, round_id):
        """
        :param round_id: int
        """
        return self.get_round(round_id)["combined_model"]

    def get_initial_model(self):
        return str(self.id)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_devices(self):
        return self.devices

    def get_rounds(self):
        return self.rounds

    def to_json(self):
        return {
            "name" : self.name,
            "ID" : self.id,
            "devices" : self.devices,
            "rounds" : self.rounds
        }

    @staticmethod
    def save_to_db(group, db_):
        """
        :param group: FL group to save to DB
        :param db_: database
        """
        return db_.create_or_update_object(group.get_id(), group.to_json())

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
            id=json_data["ID"],
            devices=json_data["devices"],
            rounds=json_data["rounds"])
