from .db_object import DBObject

class Device(DBObject):

    def __init__(self, id, registered_on):
        """
        :param id: string
        :param registered_on: string
        """
        self.id = id
        self.registered_on = registered_on

    def get_id(self):
        return self.id

    def get_registered_on(self):
        return self.registered_on

    def to_json(self):
        return {
            "ID" : self.id,
            "registered_on" : self.registered_on
        }

    @staticmethod
    def from_json(json_data):
        return Device(json_data["ID"], json_data["registered_on"])
