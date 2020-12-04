from fedlearn_auth import get_id_from_token, verify_jwt_token, verify_key

from ...auth import AuthPolicy
from ...model import ApiKey, ApiKeyTypeEnum, DBObject
from ...model.user_factory import UserFactory
from ..utils.user import handle_load_user


def auth_controller(event, key_db, user_db):
    token_id = get_id_from_token(event.get_token())
    principalId = "user|" + token_id

    policy = AuthPolicy(principalId, event.get_aws_account_id())
    policy.restApiId = event.get_rest_api_id()
    policy.region = event.get_region()
    policy.stage = event.get_stage()

    authenticated = False
    authentication_type = "UNAUTHENTICATED"
    entity_id = "UNAUTHENTICATED"
    try:
        auth_token_api_key = DBObject.load_from_db(ApiKey, token_id, key_db)
        authentication_type = auth_token_api_key.key_type.value
        if ApiKeyTypeEnum(authentication_type) == ApiKeyTypeEnum.DEVICE:
            entity_id = auth_token_api_key.id
        else:
            entity_id = auth_token_api_key.entity_id

        authenticated = verify_key(
            event.get_token(),
            auth_token_api_key.hash)
    except BaseException:
        authenticated, entity_id = verify_jwt_token(event.get_token())

        # If the user authenticated using a JWT, make sure we set that here.
        if authenticated:
            authentication_type = ApiKeyTypeEnum.JWT.value

    if authenticated and ApiKeyTypeEnum(authentication_type) != ApiKeyTypeEnum.DEVICE:
        # If the user doesn't exist in the user DB, we want to add them
        user = handle_load_user(user_db, entity_id)
        if not user:
            new_user = UserFactory.create_user(entity_id)
            new_user.save_to_db(user_db)

    if authenticated:
        policy.allowAllMethods()
    else:
        policy.denyAllMethods()

    auth_response = policy.build()
    auth_response["context"] = {
        "entity_id": entity_id,
        "authentication_type": authentication_type
    }

    return auth_response
