import boto3
import botocore

from tests import test_create_group_function

# Note: Requires AWS SAM to be running locally before this can run

if __name__ == '__main__':
    test_create_group_function()
