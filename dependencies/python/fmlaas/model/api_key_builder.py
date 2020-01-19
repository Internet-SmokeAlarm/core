from .api_key import ApiKey
from .builder import Builder

from ..utils.time import get_epoch_time
from ..auth import generate_key_pair

class ApiKeyBuilder(Builder):

    def __init__(self):
        self.id, self.key = generate_key_pair()
        self.created_on = get_epoch_time()
        self.event_log = {}

    def build(self):
        self._validate_paramaters()

        return ApiKey(self.id, self.key, self.created_on, self.event_log)

    def _validate_paramaters(self):
        # No parameters *yet*...
        return True
