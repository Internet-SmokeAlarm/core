import json

from fmlaas import get_auth_key_table_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.exception import RequestForbiddenException
from fmlaas.controller.create_api_key import create_api_key_controller

def lambda_handler(event, context):
    auth_json = event["requestContext"]["authorizer"]
    # TODO : Once authentication can handle JWT & user functionality gets developed,
    #   remove following alteration.
    auth_json["entity_id"] = json.loads(event.get("body"))["user_id"]

    # **WARNING**: For now, passing User ID information inside the request.
    #   This sidesteps the problem of having to set up user pools right now, before
    #   implementation has been worked out. Once that gets decided, we need to come
    #   back here and fix the glaring security flaws associated with this strategy.
    dynamodb_ = DynamoDBInterface(get_auth_key_table_from_env())

    try:
        key_plaintext = create_api_key_controller(dynamodb_, auth_json)

        return {
            "statusCode" : 200,
            "body" : json.dumps({"key" : key_plaintext})
        }
    except RequestForbiddenException as error:
        return {
            "statusCode" : 401,
            "body" : str(error)
        }
