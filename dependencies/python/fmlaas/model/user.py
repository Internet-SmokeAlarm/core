from typing import List
from typing import Any
from typing import Dict
from .db_object import DBObject


class User(DBObject):

    def __init__(self,
                 username: str,
                 projects: List[Dict[str, str]],
                 api_keys: List[str]):
        self._username = username
        self._projects = projects
        self._api_keys = api_keys

    def get_id(self) -> str:
        return self.username

    @property
    def username(self) -> str:
        return self._username

    @property
    def projects(self) -> List[Dict[str, str]]:
        return self._projects

    @property
    def api_keys(self) -> List[str]:
        return self._api_keys

    def add_project(self, id: str, name: str):
        self._projects.append({
            "id": id,
            "name": name
        })

    def add_api_key(self, id: str):
        self._api_keys.append(id)

    def to_json(self) -> Dict[str, Any]:
        return {
            "ID": self._username,
            "projects": self._projects,
            "api_keys": self._api_keys
        }

    def __eq__(self, other):
        return (type(other) == type(self)) and (self.username == other.username) and (self.projects == other.projects) and (self.api_keys == other.api_keys)

    @staticmethod
    def from_json(json_data: Dict[str, Any]):
        return User(json_data["ID"],
                    json_data["projects"],
                    json_data["api_keys"])
