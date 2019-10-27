import json
import boto3
import os
from utils import generate_group_id

def add_group(group_id, group_name):
    """
    :param group_id: int
    :param group_name: string
    """
    TABLE_NAME = os.environ["GROUPS_TABLE_NAME"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    table.put_item(Item={
        "ID" : group_id,
        "Group Name" : group_name,
        "Learning Round IDs" : []
    })

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    group_name = req_json["group_name"]

    # TODO : Authenticate user

    group_id = generate_group_id()
    add_group(group_id, group_name)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"group_id" : group_id})
    }
