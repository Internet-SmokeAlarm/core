from .api_key import ApiKey
from .builder import Builder
from ..utils.time import get_epoch_time

class ApiKeyBuilder(Builder):

    def __init__(self, id, hash):
        """
        :param id: string. Non-hashed key ID
        :param hash: string. Hashed key
        """
        self.id = id
        self.hash = hash
        self.created_on = get_epoch_time()
        self.event_log = {}
        self.key_type = None
        self.entity_id = None

    def set_key_type(self, key_type):
        """
        :param permissions_group: string
        """
        self.key_type = key_type

    def set_entity_id(self, entity_id):
        """
        :param entity_id: string
        """
        self.entity_id = entity_id

    def build(self):
        self._validate_paramaters()

        return ApiKey(self.id,
            self.hash,
            self.created_on,
            self.event_log,
            self.key_type,
            self.entity_id)

    def _validate_paramaters(self):
        if self.key_type == None:
            raise ValueError("Key type must not be None")
        elif type(self.key_type) is not type("str"):
            raise ValueError("Key type must be of type string")

        if self.entity_id == None:
            raise ValueError("Entity ID must not be None")
        elif type(self.entity_id) is not type("str"):
            raise ValueError("Entity ID must be of type string")
