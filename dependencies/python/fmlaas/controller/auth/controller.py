from ...generate_unique_id import generate_unique_id
from ...auth import AuthPolicy
from ...auth import HttpVerb
from ...auth import PermissionsGroupTypeEnum
from ...auth import get_id_from_token
from ...auth import verify_key
from ...model import DBObject
from ...auth.model import ApiKey
from ...request_processor import IDProcessor
from ...auth import get_resource_list

def auth_controller(event, key_db):
    id_processor = IDProcessor(event.get_path_parameters())
    group_id = id_processor.get_group_id(throw_exception=False)
    round_id = id_processor.get_round_id(throw_exception=False)
    device_id = id_processor.get_device_id(throw_exception=False)

    token_id = get_id_from_token(event.get_token())
    principalId = "user|" + token_id

    policy = AuthPolicy(principalId, event.get_aws_account_id())
    policy.restApiId = event.get_rest_api_id()
    policy.region = event.get_region()
    policy.stage = event.get_stage()

    #base_path = event.get_method_arn().split('/')[0] + "/" + event.get_stage() + "/"

    # TODO: Handle JWT from Cognito as well as API keys here
    try:
        auth_token_api_key = DBObject.load_from_db(ApiKey, token_id, key_db)
        permissions_group = auth_token_api_key.get_permissions_group()
        verified_authenticated = verify_key(event.get_token(), auth_token_api_key.get_hash())
    except:
        permissions_group = PermissionsGroupTypeEnum.UNAUTHENTICATED
        verified_authenticated = False

    if permissions_group != PermissionsGroupTypeEnum.UNAUTHENTICATED and verified_authenticated:
        for resource in get_resource_list(permissions_group, group_id, round_id, device_id):
            policy.allowMethod(HttpVerb.ALL, resource)
    else:
        policy.denyAllMethods()

    return policy.build()
