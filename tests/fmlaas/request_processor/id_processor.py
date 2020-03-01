import unittest

from dependencies.python.fmlaas.request_processor import IDProcessor

class IDProcessorTestCase(unittest.TestCase):

    def test_get_group_name_fail(self):
        json_data = {"group_name" : None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_group_name)

    def test_get_group_name_fail_2(self):
        json_data = {"group_name" : 12334}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_group_name)

    def test_get_group_name_fail_3(self):
        id_processor = IDProcessor({})
        self.assertIsNone(id_processor.get_group_name(throw_exception=False))

    def test_get_round_id_fail(self):
        json_data = {"round_id" : None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_round_id)

    def test_get_round_id_fail_2(self):
        json_data = {"round_id" : 12334}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_round_id)

    def test_get_round_id_fail_3(self):
        id_processor = IDProcessor({})
        self.assertIsNone(id_processor.get_round_id(throw_exception=False))

    def test_get_group_id_fail(self):
        json_data = {"group_id" : None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_group_id)

    def test_get_group_id_fail_2(self):
        json_data = {"group_id" : 12334}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_group_id)

    def test_get_group_id_fail_3(self):
        id_processor = IDProcessor({})
        self.assertIsNone(id_processor.get_group_id(throw_exception=False))

    def test_get_device_id_fail(self):
        json_data = {"device_id" : None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_device_id)

    def test_get_device_id_fail_2(self):
        json_data = {"device_id" : 12334}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_device_id)

    def test_get_device_id_fail_3(self):
        id_processor = IDProcessor({})
        self.assertIsNone(id_processor.get_device_id(throw_exception=False))

    def test_get_group_name_pass(self):
        json_data = {"group_name" : "None"}
        id_processor = IDProcessor(json_data)

        self.assertEqual("None", id_processor.get_group_name())

    def test_get_previous_round_id_pass(self):
        json_data = {"previous_round_id" : "None"}
        id_processor = IDProcessor(json_data)

        self.assertEqual("None", id_processor.get_previous_round_id())

    def test_get_previous_round_id_fail_1(self):
        json_data = {"previous_round_id" : None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_previous_round_id)

    def test_get_previous_round_id_fail_2(self):
        json_data = {"previous_round_id" : 10}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_previous_round_id)

    def test_get_previous_round_id_fail_3(self):
        json_data = {"previous_round_id" : None}
        id_processor = IDProcessor(json_data)

        self.assertIsNone(id_processor.get_previous_round_id(throw_exception=False))
