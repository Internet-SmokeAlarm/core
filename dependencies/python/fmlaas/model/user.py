from typing import Any
from typing import Dict, Set
from .db_object import DBObject


class User(DBObject):

    def __init__(self,
                 username: str,
                 projects: Dict[str, dict],
                 api_keys: Set[str]):
        super(User, self).__init__(username)

        self._projects = projects
        self._api_keys = api_keys

    @property
    def username(self) -> str:
        return self._id

    @property
    def projects(self) -> Dict[str, dict]:
        return self._projects

    @property
    def api_keys(self) -> Set[str]:
        return self._api_keys

    def add_project(self, id: str, name: str) -> None:
        self._projects[id] = {
            "id": id,
            "name": name
        }

    def add_api_key(self, api_key_id: str) -> None:
        self._api_keys.add(api_key_id)

    def contains_api_key(self, id: str) -> bool:
        return id in self._api_keys

    def remove_api_key(self, id: str) -> None:
        self._api_keys.remove(id)

    def to_json(self) -> Dict[str, Any]:
        return {
            "ID": self._id,
            "projects": self._projects,
            "api_keys": list(self._api_keys)
        }

    def __eq__(self, other) -> bool:
        return (type(other) == type(self)) and \
            (self._id == other._id) and \
            (self._projects == other._projects) and \
            (self._api_keys == other._api_keys)

    @staticmethod
    def from_json(json_data: Dict[str, Any]):
        return User(json_data["ID"],
                    json_data["projects"],
                    set(json_data["api_keys"]))
