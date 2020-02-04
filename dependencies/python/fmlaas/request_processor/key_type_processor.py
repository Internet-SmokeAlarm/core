from .request_processor import RequestProcessor
from ..model import ApiKeyTypeEnum

class KeyTypeProcessor(RequestProcessor):

    KEY_TYPE_KEY = "KEY_TYPE"

    def __init__(self, req_json):
        self.req_json = req_json

    def get_key_type(self, throw_exception=True):
        key_type = self.req_json.get(KeyTypeProcessor.KEY_TYPE_KEY, None)

        if not self._is_string_name_valid(key_type) and throw_exception:
            raise ValueError("Key type invalid.")

        return ApiKeyTypeEnum(key_type)
