import json

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    group_name = req_json["group_name"]

    # TODO : Generate Group Key

    return {
        "statusCode" : 200,
        "body" : json.dumps({"group_key" : "GROUP_KEY"})
    }
