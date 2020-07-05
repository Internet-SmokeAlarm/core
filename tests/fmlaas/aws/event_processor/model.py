import unittest
from dependencies.python.fmlaas.s3_storage import DeviceModelPointer
from dependencies.python.fmlaas.aws.event_processor import ModelUploadEventProcessor


class ModelUploadEventProcessorTestCase(unittest.TestCase):

    def test_process_event_pass(self):
        json_data = {
            "Records": [
                {
                    "eventVersion": "2.0",
                    "eventSource": "aws:s3",
                    "awsRegion": "us-east-1",
                    "eventTime": "1970-01-01T00:00:00.000Z",
                    "eventName": "ObjectCreated:Put",
                    "userIdentity": {
                        "principalId": "EXAMPLE"
                    },
                    "requestParameters": {
                        "sourceIPAddress": "127.0.0.1"
                    },
                    "responseElements": {
                        "x-amz-request-id": "EXAMPLE123456789",
                        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
                    },
                    "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "testConfigRule",
                        "bucket": {
                            "name": "example-bucket",
                            "ownerIdentity": {
                                "principalId": "EXAMPLE"
                            },
                            "arn": "arn:aws:s3:::example-bucket"
                        },
                        "object": {
                            "key": "1234/3434/4356/device_models/device-id-123",
                            "size": 1024,
                            "eTag": "0123456789abcdef0123456789abcdef",
                            "experimentr": "0A1B2C3D4E5F678901"
                        }
                    }
                }
            ]
        }

        models = ModelUploadEventProcessor().process_event(json_data)

        self.assertEqual(1, len(models))
        self.assertEqual("1024", models[0].get_size())
        self.assertEqual(DeviceModelPointer("1234", "3434", "4356", "device-id-123"), models[0].get_name())
