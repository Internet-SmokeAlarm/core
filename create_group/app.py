import json
from utils import generate_group_key

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    group_name = req_json["group_name"]

    # TODO : Authenticate user
    # TODO : Validate input

    group_key = generate_group_key(group_name)

    # TODO : Store group key

    return {
        "statusCode" : 200,
        "body" : json.dumps({"group_key" : group_key})
    }
