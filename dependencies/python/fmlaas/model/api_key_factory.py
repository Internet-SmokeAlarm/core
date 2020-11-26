from typing import Tuple

from fedlearn_auth import generate_key_pair, hash_secret

from ..utils.time import get_epoch_time
from .api_key import ApiKey
from .api_key_type import ApiKeyTypeEnum


class ApiKeyFactory:

    @staticmethod
    def create_api_key(entity_id: str,
                       key_type: ApiKeyTypeEnum) -> Tuple[ApiKey, str]:
        created_at = get_epoch_time()
        event_log = dict()
        id, plaintext = generate_key_pair()
        hash = hash_secret(plaintext)

        return ApiKey(id,
                      hash,
                      created_at,
                      event_log,
                      key_type,
                      entity_id), plaintext
