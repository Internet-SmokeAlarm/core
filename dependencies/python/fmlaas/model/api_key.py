from .db_object import DBObject


class ApiKey(DBObject):

    def __init__(self, id, hash, created_on, event_log, key_type, entity_id):
        """
        :param id: string
        :param hash: string
        :param created_on: string
        :param event_log: dict
        :param key_type: string
        :param entity_id: string
        """
        self.id = id
        self.hash = hash
        self.created_on = created_on
        self.event_log = event_log
        self.key_type = key_type
        self.entity_id = entity_id

    def get_id(self):
        return self.id

    def get_hash(self):
        return self.hash

    def get_created_on(self):
        return self.created_on

    def get_event_log(self):
        return self.event_log

    def get_key_type(self):
        return self.key_type

    def get_entity_id(self):
        return self.entity_id

    def to_json(self):
        return {
            "ID": self.id,
            "hash": self.hash,
            "created_on": self.created_on,
            "event_log": self.event_log,
            "key_type": self.key_type,
            "entity_id": self.entity_id
        }

    @staticmethod
    def from_json(json_data):
        return ApiKey(json_data["ID"],
                      json_data["hash"],
                      json_data["created_on"],
                      json_data["event_log"],
                      json_data["key_type"],
                      json_data["entity_id"])
