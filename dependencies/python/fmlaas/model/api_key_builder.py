from .api_key import ApiKey
from .builder import Builder

from ..utils.time import get_epoch_time
from ..auth import generate_key_pair

class ApiKeyBuilder(Builder):

    def __init__(self):
        self.id, self.key = generate_key_pair()
        self.created_on = get_epoch_time()
        self.event_log = {}
        self.permissions_group = None

    def set_permissions_group(self, permissions_group):
        """
        :param permissions_group: PermissionGroupTypeEnum
        """
        self.permissions_group = permissions_group.value

    def build(self):
        self._validate_paramaters()

        return ApiKey(self.id, self.key, self.created_on, self.event_log, self.permissions_group)

    def _validate_paramaters(self):
        if self.permissions_group == None:
            raise ValueError("Permissions Group must not be None")
        elif type(self.permissions_group) is not type("str"):
            raise ValueError("Permissions Group must be of type PermissionGroupTypeEnum")
