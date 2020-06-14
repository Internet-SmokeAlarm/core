from .request_processor import RequestProcessor
from ..model import ApiKeyTypeEnum


class AuthContextProcessor(RequestProcessor):

    AUTH_TYPE_KEY = "authentication_type"
    ENTITY_ID_KEY = "entity_id"

    def __init__(self, auth_json):
        self.auth_json = auth_json

    def get_type(self, throw_exception=True):
        auth_type = self.auth_json.get(
            AuthContextProcessor.AUTH_TYPE_KEY, None)

        if not self._is_string_name_valid(auth_type) and throw_exception:
            raise ValueError("Auth type invalid.")

        return ApiKeyTypeEnum(auth_type)

    def get_entity_id(self, throw_exception=True):
        entity_id = self.auth_json.get(
            AuthContextProcessor.ENTITY_ID_KEY, None)

        if not self._is_string_name_valid(entity_id) and throw_exception:
            raise ValueError("Entity ID invalid.")

        return entity_id

    def is_type_user(self):
        return self.get_type() == ApiKeyTypeEnum.USER or self.get_type() == ApiKeyTypeEnum.JWT

    def is_type_device(self):
        return self.get_type() == ApiKeyTypeEnum.DEVICE
