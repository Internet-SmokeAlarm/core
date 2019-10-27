import json
import boto3
import os

from utils import generate_device_key_pair

def add_device(device_id, device_api_key):
    TABLE_NAME = os.environ["DEVICE_TABLE_NAME"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    table.put_item(Item={
        "ID" : device_id,
        "APIKey" : device_api_key
    })

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))

    # TODO : Authenticate user

    device_id, device_api_key = generate_device_key_pair()

    add_device(device_id, device_api_key)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"device_id" : device_id, "device_api_key" : device_api_key})
    }
