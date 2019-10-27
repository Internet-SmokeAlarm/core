import json
import boto3
import os

from utils import generate_round_key

def add_round(round_id):
    """
    :param round_id: int
    """
    TABLE_NAME = os.environ["LEARNING_ROUND_TABLE_NAME"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    table.put_item(Item={
        "ID" : round_id,
        "model_updates" : []
    })

def add_round_id_to_group(group_id, round_id):
    """
    :param group_id: int
    :param round_id: int
    """
    TABLE_NAME = os.environ["GROUPS_TABLE_NAME"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    group_item = table.get_item(Key={"ID" : group_id})["Item"]
    group_item["Learning Round IDs"].append(round_id)

    table.put_item(Item=group_item)

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    group_id = req_json["group_id"]

    # TODO : Authenticate user

    round_id = generate_round_key()
    add_round(round_id)
    add_round_id_to_group(group_id, round_id)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"round_id" : round_id})
    }
