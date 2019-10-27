import boto3
import json
import os

def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """
    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    response = s3_client.generate_presigned_post(Bucket=bucket_name,
                                                 Key=object_name,
                                                 Fields=fields,
                                                 Conditions=conditions,
                                                 ExpiresIn=expiration)

    return response

def generate_object_name(device_id, round_number):
    """
    Generates appropriate S3 object name given state information.

    :param device_id: int
    :param round_number: int
    """
    return str(device_id) + "_" + str(round_number)

def add_model_to_db(round_id, device_id, object_name):
    """
    :param round_id: int
    :param device_id: int
    :param object_name: string
    """
    TABLE_NAME = os.environ["LEARNING_ROUND_TABLE_NAME"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    round_item = table.get_item(Key={"ID" : round_id})["Item"]

    round_item["model_updates"].append({
        "device_id" : device_id,
        "model" : object_name})

    table.put_item(Item=round_item)

def lambda_handler(event, context):
    BUCKET_NAME = os.environ["MODELS_BUCKET"]

    req_json = json.loads(event.get('body'))
    round_id = req_json["round_id"]
    device_id = req_json["device_id"]

    # TODO : Authenticate user

    object_name = generate_object_name(device_id, round_id)
    add_model_to_db(round_id, device_id, object_name)

    fields = {}
    conditions = []
    expiration_sec = 60 * 30

    presigned_url = create_presigned_post(BUCKET_NAME, object_name,
                                          fields, conditions, expiration=expiration_sec)

    return {
        "statusCode" : 200,
        "body" : json.dumps({"model_url" : presigned_url})
    }
