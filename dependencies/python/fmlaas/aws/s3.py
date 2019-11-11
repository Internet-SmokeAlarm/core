import boto3
import os

def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    NOTE: This was directly taken from AWS documentation.
    (https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html)

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

def get_models_bucket_name():
    return os.environ["MODELS_BUCKET"]
