import unittest

from dependencies.python.fmlaas.request_processor import IDProcessor

class RequestProcessorTestCase(unittest.TestCase):

    def test_is_string_name_valid_fail(self):
        json_data = {"group_name" : None}
        id_processor = IDProcessor(json_data)

        self.assertFalse(id_processor._is_string_name_valid(json_data["group_name"]))

    def test_is_string_name_valid_pass(self):
        json_data = {"group_name" : "None"}
        id_processor = IDProcessor(json_data)

        self.assertTrue(id_processor._is_string_name_valid(json_data["group_name"]))

    def test_is_string_name_valid_fail_2(self):
        json_data = {"group_name" : 110000}
        id_processor = IDProcessor(json_data)

        self.assertFalse(id_processor._is_string_name_valid(json_data["group_name"]))

    def test_is_int_name_valid_pass(self):
        json_data = {"group_name" : 10}
        id_processor = IDProcessor(json_data)

        self.assertTrue(id_processor._is_int_name_valid(json_data["group_name"]))

    def test_is_int_name_valid_fail(self):
        json_data = {"group_name" : "None"}
        id_processor = IDProcessor(json_data)

        self.assertFalse(id_processor._is_int_name_valid(json_data["group_name"]))

    def test_is_int_name_valid_fail_2(self):
        json_data = {"group_name" : None}
        id_processor = IDProcessor(json_data)

        self.assertFalse(id_processor._is_int_name_valid(json_data["group_name"]))
