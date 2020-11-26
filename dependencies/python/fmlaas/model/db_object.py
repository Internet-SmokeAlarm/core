from abc import abstractmethod

from ..database import DB


class DBObject:

    def __init__(self, id: str):
        self._id = id

    @staticmethod
    def load_from_db(object_class: any, id: str, db_: DB) -> any:
        return object_class.from_json(db_.get_object(id))

    @property
    def id(self) -> int:
        return self._id

    @abstractmethod
    def to_json(self) -> dict:
        raise NotImplementedError("to_json() not implemented")

    def save_to_db(self, db_: DB) -> bool:
        return db_.create_or_update_object(self._id, self.to_json())
