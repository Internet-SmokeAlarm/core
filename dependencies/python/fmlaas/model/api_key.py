from .db_object import DBObject

class ApiKey(DBObject):

    def __init__(self, id, hash, created_on, event_log):
        """
        :param id: string
        :param hash: string
        :param created_on: string
        :param event_log: dict
        """
        self.id = id
        self.hash = hash
        self.created_on = created_on
        self.event_log = event_log

    def get_id(self):
        return self.id

    def get_hash(self):
        return self.hash

    def get_created_on(self):
        return self.created_on

    def get_event_log(self):
        return self.event_log

    def to_json(self):
        return {
            "ID" : self.id,
            "hash" : self.hash,
            "created_on" : self.created_on,
            "event_log" : self.event_log
        }

    @staticmethod
    def from_json(json_data):
        return ApiKey(json_data["ID"],
            json_data["hash"],
            json_data["created_on"],
            json_data["event_log"])
