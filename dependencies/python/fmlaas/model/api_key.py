from .api_key_type import ApiKeyTypeEnum
from .db_object import DBObject


class ApiKey(DBObject):

    def __init__(self,
                 id: str,
                 hash: str,
                 created_at: int,
                 event_log: dict,
                 key_type: ApiKeyTypeEnum,
                 entity_id: str):
        super(ApiKey, self).__init__(id)

        self._hash = hash
        self._created_at = created_at
        self._event_log = event_log
        self._key_type = key_type
        self._entity_id = entity_id

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def created_at(self) -> int:
        return self._created_at

    @property
    def event_log(self) -> dict:
        return self._event_log

    @property
    def key_type(self) -> ApiKeyTypeEnum:
        return self._key_type

    @property
    def entity_id(self) -> str:
        return self._entity_id

    def to_json(self) -> dict:
        return {
            "ID": self._id,
            "hash": self._hash,
            "created_at": str(self._created_at),
            "event_log": self._event_log,
            "key_type": self._key_type.value,
            "entity_id": self._entity_id
        }

    @staticmethod
    def from_json(json_data):
        return ApiKey(json_data["ID"],
                      json_data["hash"],
                      int(json_data["created_at"]),
                      json_data["event_log"],
                      ApiKeyTypeEnum(json_data["key_type"]),
                      json_data["entity_id"])

    def __eq__(self, other) -> bool:
        # NOTE: We can't test the hash here, so we only test the other attributes.
        
        return (type(self) == type(other)) and \
            (self._id == other._id) and \
            (self._created_at == other._created_at) and \
            (self._event_log == other._event_log) and \
            (self._key_type == other._key_type) and \
            (self._entity_id == other._entity_id)