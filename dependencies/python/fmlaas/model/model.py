from ..s3_storage import PointerFactory


class Model:

    def __init__(self,
                 entity_id: str,
                 name: str,
                 size: int):
        self._entity_id = entity_id
        self._name = name
        self._size = size

    @property
    def entity_id(self) -> str:
        return self._entity_id
    
    @entity_id.setter
    def entity_id(self, value: str) -> None:
        self._entity_id = value

    @property
    def name(self) -> str:
        return PointerFactory.load_pointer(self._name)

    @property
    def size(self) -> int:
        return self._size

    def to_json(self) -> dict:
        return {
            "entity_id": self._entity_id,
            "name": self._name,
            "size": str(self._size)
        }

    @staticmethod
    def from_json(json_data):
        return Model(json_data["entity_id"],
                     json_data["name"],
                     int(json_data["size"]))

    @staticmethod
    def is_valid_json(json_data: dict) -> bool:
        return "entity_id" in json_data and \
            "name" in json_data and \
            "size" in json_data

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and \
            (self._entity_id == other._entity_id) and \
            (self._name == other._name) and \
            (self._size == other._size)
