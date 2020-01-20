import unittest

from dependencies.python.fmlaas.controller.auth import auth_controller
from dependencies.python.fmlaas.auth.model import ApiKey
from dependencies.python.fmlaas.auth.model import ApiKeyBuilder
from dependencies.python.fmlaas.aws.event_processor import AuthEventProcessor
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.auth import PermissionsGroupTypeEnum

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
                "group_id" : "1234",
                "round_id" : "3453533",
                "device_id" : "1231214"
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

        builder = ApiKeyBuilder()
        builder.set_permissions_group(PermissionsGroupTypeEnum.USER)
        api_key = builder.build()
        key_string = builder.get_api_key()

        api_key.save_to_db(key_db)

        auth_event = self._build_default_event(key_string)
        result = auth_controller(auth_event, key_db)

        self.assertEqual(result["policyDocument"]["Statement"][0]["Effect"], "Allow")
        self.assertEqual(len(result["policyDocument"]["Statement"][0]["Resource"]), 2)

    def test_auth_controller_pass_2(self):
        key_db = InMemoryDBInterface()

        builder = ApiKeyBuilder()
        builder.set_permissions_group(PermissionsGroupTypeEnum.GROUP_ADMIN)
        api_key = builder.build()
        key_string = builder.get_api_key()

        api_key.save_to_db(key_db)
        auth_event = self._build_default_event(key_string)

        result = auth_controller(auth_event, key_db)

        self.assertEqual(result["policyDocument"]["Statement"][0]["Effect"], "Allow")
        self.assertEqual(len(result["policyDocument"]["Statement"][0]["Resource"]), 10)

    def test_auth_controller_pass_3(self):
        key_db = InMemoryDBInterface()

        builder = ApiKeyBuilder()
        builder.set_permissions_group(PermissionsGroupTypeEnum.GROUP_MEMBER)
        api_key = builder.build()
        key_string = builder.get_api_key()

        api_key.save_to_db(key_db)
        auth_event = self._build_default_event(key_string)

        result = auth_controller(auth_event, key_db)

        self.assertEqual(result["policyDocument"]["Statement"][0]["Effect"], "Allow")
        self.assertEqual(len(result["policyDocument"]["Statement"][0]["Resource"]), 10)

    def test_auth_controller_pass_4(self):
        key_db = InMemoryDBInterface()

        builder = ApiKeyBuilder()
        builder.set_permissions_group(PermissionsGroupTypeEnum.GROUP_READ_ONLY_MEMBER)
        api_key = builder.build()
        key_string = builder.get_api_key()

        api_key.save_to_db(key_db)
        auth_event = self._build_default_event(key_string)

        result = auth_controller(auth_event, key_db)

        self.assertEqual(result["policyDocument"]["Statement"][0]["Effect"], "Allow")
        self.assertEqual(len(result["policyDocument"]["Statement"][0]["Resource"]), 7)

    def test_auth_controller_pass_5(self):
        key_db = InMemoryDBInterface()

        builder = ApiKeyBuilder()
        builder.set_permissions_group(PermissionsGroupTypeEnum.GROUP_DEVICE)
        api_key = builder.build()
        key_string = builder.get_api_key()

        api_key.save_to_db(key_db)
        auth_event = self._build_default_event(key_string)

        result = auth_controller(auth_event, key_db)

        self.assertEqual(result["policyDocument"]["Statement"][0]["Effect"], "Allow")
        self.assertEqual(len(result["policyDocument"]["Statement"][0]["Resource"]), 5)

    def test_auth_controller_pass_6(self):
        key_db = InMemoryDBInterface()

        builder = ApiKeyBuilder()
        builder.set_permissions_group(PermissionsGroupTypeEnum.UNAUTHENTICATED)
        api_key = builder.build()
        key_string = builder.get_api_key()

        api_key.save_to_db(key_db)
        auth_event = self._build_default_event(key_string)

        result = auth_controller(auth_event, key_db)

        self.assertEqual(result["policyDocument"]["Statement"][0]["Effect"], "Deny")
        self.assertEqual(len(result["policyDocument"]["Statement"][0]["Resource"]), 1)
