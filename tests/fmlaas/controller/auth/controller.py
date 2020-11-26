import unittest
from dependencies.python.fedlearn_auth import generate_key_pair
from dependencies.python.fedlearn_auth import hash_secret
from dependencies.python.fmlaas.controller.auth import auth_controller
from dependencies.python.fmlaas.model import ApiKey
from dependencies.python.fmlaas.model import ApiKeyFactory
from dependencies.python.fmlaas.aws.event_processor import AuthEventProcessor
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.database import InMemoryDBInterface


class AuthControllerTestCase(unittest.TestCase):

    def _build_default_event(self, key_string):
        req_json = {
            "type": "REQUEST",
            "methodArn": "arn:aws:execute-api:us-east-1:123456789012:s4x3opwd6i/Prod/POST/v1/group/get/current_round_id/1234",
            "resource": "/request",
            "path": "/request",
            "httpMethod": "GET",
            "headers": {
                "X-AMZ-Date": "20170718T062915Z",
                "Accept": "*/*",
                "Authorization": key_string,
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
                "group_id": "1234",
                "round_id": "3453533",
                "device_id": "1231214"
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
        return AuthEventProcessor().process_event(req_json)

    def test_auth_controller_pass_1(self):
        key_db = InMemoryDBInterface()

        id, key_plaintext = generate_key_pair()
        key_hash = hash_secret(key_plaintext)
        builder = ApiKeyFactory(id, key_hash)
        builder.set_entity_id("123123")
        builder.set_key_type("USER")
        api_key = builder.build()

        api_key.save_to_db(key_db)

        auth_event = self._build_default_event(key_plaintext)
        result = auth_controller(auth_event, key_db)

        self.assertEqual(
            result["context"]["entity_id"],
            api_key.get_entity_id())
        self.assertEqual(result["policyDocument"]
                         ["Statement"][0]["Effect"], "Allow")

    def test_auth_controller_pass_2(self):
        key_db = InMemoryDBInterface()

        id, key_plaintext = generate_key_pair()
        key_hash = hash_secret(key_plaintext)
        builder = ApiKeyFactory(id, key_hash)
        builder.set_entity_id("123123")
        builder.set_key_type("USER")
        api_key = builder.build()

        api_key.save_to_db(key_db)
        auth_event = self._build_default_event(key_plaintext)

        result = auth_controller(auth_event, key_db)

        self.assertEqual(
            result["context"]["entity_id"],
            api_key.get_entity_id())
        self.assertEqual(result["policyDocument"]
                         ["Statement"][0]["Effect"], "Allow")

    def test_auth_controller_pass_3(self):
        key_db = InMemoryDBInterface()

        id, key_plaintext = generate_key_pair()
        key_hash = hash_secret(key_plaintext)
        builder = ApiKeyFactory(id, key_hash)
        builder.set_entity_id("123123")
        builder.set_key_type("DEVICE")
        api_key = builder.build()

        api_key.save_to_db(key_db)
        auth_event = self._build_default_event(key_plaintext)

        result = auth_controller(auth_event, key_db)

        self.assertEqual(result["context"]["entity_id"], api_key.get_id())
        self.assertEqual(
            result["context"]["authentication_type"],
            api_key.get_key_type())
        self.assertEqual(result["policyDocument"]
                         ["Statement"][0]["Effect"], "Allow")
