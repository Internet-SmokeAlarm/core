class Device:

    def __init__(self,
                id: str,
                registered_at: int):
        self._id = id
        self._registered_at = registered_at
    
    @property
    def id(self) -> str:
        return self._id

    @property
    def registered_at(self) -> int:
        return self._registered_at

    def to_json(self):
        return {
            "ID": self._id,
            "registered_at": str(self._registered_at)
        }

    @staticmethod
    def from_json(json_data):
        return Device(json_data["ID"],
                      int(json_data["registered_at"]))
    
    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and \
            (self._id == other._id) and \
            (self._registered_at == other._registered_at)
