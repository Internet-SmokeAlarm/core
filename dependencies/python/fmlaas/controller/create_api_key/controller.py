from ...model import ApiKeyBuilder
from ...model import ApiKeyTypeEnum
from ...exception import raise_default_request_forbidden_error
from fedlearn_auth import generate_key_pair
from fedlearn_auth import hash_secret
from ..abstract_controller import AbstractController
from ..utils.auth.conditions import IsUser


class CreateApiKeyController(AbstractController):

    def __init__(self, key_db, auth_context):
        """
        :param key_db: DB
        :param auth_context: AuthContextProcessor
        """
        super(CreateApiKeyController, self).__init__(auth_context)

        self.key_db = key_db

    def get_auth_conditions(self):
        return [
            [
                IsUser()
            ]
        ]

    def execute_controller(self):
        id, key_plaintext = generate_key_pair()
        key_hash = hash_secret(key_plaintext)
        builder = ApiKeyBuilder(id, key_hash)
        builder.set_key_type(ApiKeyTypeEnum.USER.value)
        builder.set_entity_id(self.auth_context.get_entity_id())
        api_key = builder.build()

        api_key.save_to_db(self.key_db)

        return key_plaintext
