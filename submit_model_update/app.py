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

def generate_object_name(group_key, device_id, round_number):
    """
    Generates appropriate S3 object name given state information.

    :param group_key: string
    :param device_id: string
    :param round_number: integer
    """
    return group_key + "_" + device_id + "_" + str(round_number)

def lambda_handler(event, context):
    BUCKET_NAME = os.environ["MODELS_BUCKET"]

    req_json = json.loads(event.get('body'))
    group_key = req_json["group_key"]

    # TODO : Authenticate user
    # TODO : Validate input

    # TODO : Get device ID from DB
    device_id = "100ace"

    # TODO : Get current round number for group
    round_number = 0

    object_name = generate_object_name(group_key, device_id, round_number)

    fields = {}
    conditions = []
    expiration_sec = 60 * 60

    presigned_url = create_presigned_post(BUCKET_NAME, object_name,
                                          fields, conditions, expiration=expiration_sec)

    return_data = {"model_url" : presigned_url}

    return {
        "statusCode" : 200,
        "body" : json.dumps(return_data)
    }
