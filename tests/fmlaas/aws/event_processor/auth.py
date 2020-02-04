import unittest

from dependencies.python.fmlaas.model import ApiKey
from dependencies.python.fmlaas.model import ApiKeyBuilder
from dependencies.python.fmlaas.aws.event_processor import AuthEventProcessor
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fedlearn_auth import generate_key_pair
from dependencies.python.fedlearn_auth import hash_secret

class AuthEventProcessorTestCase(unittest.TestCase):

    def test_process_event_pass(self):
        id, key_plaintext = generate_key_pair()
        key_hash = hash_secret(key_plaintext)
        builder = ApiKeyBuilder(id, key_hash)
        builder.set_entity_id("123123")
        builder.set_key_type("USER")
        api_key = builder.build()

        req_json = {
            "type": "REQUEST",
            "methodArn": "arn:aws:execute-api:us-east-1:123456789012:s4x3opwd6i/Prod/POST/v1/group/get/current_round_id/1234",
            "resource": "/request",
            "path": "/request",
            "httpMethod": "GET",
            "headers": {
                "X-AMZ-Date": "20170718T062915Z",
                "Accept": "*/*",
                "Authorization": key_plaintext,
                "CloudFront-Viewer-Country": "US",
                "CloudFront-Forwarded-Proto": "https",
                "CloudFront-Is-Tablet-Viewer": "false",
                "CloudFront-Is-Mobile-Viewer": "false",
                "User-Agent": "...",
                "X-Forwarded-Proto": "https",
                "CloudFront-Is-SmartTV-Viewer": "false",
                "Host": "....execute-api.us-east-1.amazonaws.com",
                "Accept-Encoding": "gzip, deflate",
                "X-Forwarded-Port": "443",
                "X-Amzn-Trace-Id": "...",
                "Via": "...cloudfront.net (CloudFront)",
                "X-Amz-Cf-Id": "...",
                "X-Forwarded-For": "..., ...",
                "Postman-Token": "...",
                "cache-control": "no-cache",
                "CloudFront-Is-Desktop-Viewer": "true",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "queryStringParameters": {
            },
            "pathParameters": {
                "group_id" : "1234",
                "round_id" : "3453533"
            },
            "stageVariables": {
            },
            "requestContext": {
                "path": "/request",
                "accountId": "123456789012",
                "resourceId": "05c7jb",
                "stage": "test",
                "requestId": "...",
                "identity": {
                    "apiKey": "...",
                    "sourceIp": "..."
                },
                "resourcePath": "/request",
                "httpMethod": "GET",
                "apiId": "s4x3opwd6i"
            }
        }
        auth_event = AuthEventProcessor().process_event(req_json)

        self.assertEqual(key_plaintext, auth_event.get_token())
        self.assertEqual({"group_id" : "1234", "round_id" : "3453533"}, auth_event.get_path_parameters())
        self.assertEqual("arn:aws:execute-api:us-east-1:123456789012:s4x3opwd6i/Prod/POST/v1/group/get/current_round_id/1234", auth_event.get_method_arn())
        self.assertEqual("Prod", auth_event.get_stage())
        self.assertEqual("s4x3opwd6i", auth_event.get_rest_api_id())
        self.assertEqual("123456789012", auth_event.get_aws_account_id())
        self.assertEqual("us-east-1", auth_event.get_region())
