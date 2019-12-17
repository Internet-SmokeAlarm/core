import unittest

from dependencies.python.fmlaas.request_processor import RequestJSONProcessor

class RequestJSONProcessorTestCase(unittest.TestCase):

    def test_get_group_name_fail(self):
        json_data = {"group_name" : None}
        request_json_processor = RequestJSONProcessor(json_data)

        self.assertRaises(ValueError, request_json_processor.get_group_name)

    def test_get_group_name_fail_2(self):
        json_data = {"group_name" : 12334}
        request_json_processor = RequestJSONProcessor(json_data)

        self.assertRaises(ValueError, request_json_processor.get_group_name)

    def test_get_group_name_pass(self):
        json_data = {"group_name" : "None"}
        request_json_processor = RequestJSONProcessor(json_data)

        self.assertEqual("None", request_json_processor.get_group_name())

    def test_is_group_name_valid_fail(self):
        json_data = {"group_name" : None}
        request_json_processor = RequestJSONProcessor(json_data)

        self.assertFalse(request_json_processor._is_group_name_valid(json_data["group_name"]))

    def test_is_group_name_valid_pass(self):
        json_data = {"group_name" : "None"}
        request_json_processor = RequestJSONProcessor(json_data)

        self.assertTrue(request_json_processor._is_group_name_valid(json_data["group_name"]))

    def test_is_group_name_valid_fail_2(self):
        json_data = {"group_name" : 110000}
        request_json_processor = RequestJSONProcessor(json_data)

        self.assertFalse(request_json_processor._is_group_name_valid(json_data["group_name"]))
