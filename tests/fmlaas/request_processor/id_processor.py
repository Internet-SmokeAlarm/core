from dependencies.python.fmlaas.request_processor.request_processor import RequestProcessor
import unittest

from dependencies.python.fmlaas.request_processor import IDProcessor


class IDProcessorTestCase(unittest.TestCase):

    def test_get_experiment_id_fail(self):
        json_data = {"experiment_id": None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_experiment_id)

    def test_get_experiment_id_fail_2(self):
        json_data = {"experiment_id": 1234}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_experiment_id)

    def test_get_experiment_id_fail_3(self):
        json_data = {}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_experiment_id)

    def test_get_experiment_id_pass(self):
        json_data = {"experiment_id": "experimentid1234234"}
        id_processor = IDProcessor(json_data)

        self.assertEqual("experimentid1234234", id_processor.get_experiment_id())
    
    def test_get_experiment_name_pass(self):
        json_data = {"experiment_name": "experiment_name_1234234"}
        id_processor = IDProcessor(json_data)

        self.assertEqual("experiment_name_1234234", id_processor.get_experiment_name())
    
    def test_get_experiment_description_pass(self):
        json_data = {"experiment_description": "Descriptions are cool!"}
        id_processor = IDProcessor(json_data)

        self.assertEqual("Descriptions are cool!", id_processor.get_experiment_description())
    
    def test_get_experiment_description_pass_2(self):
        id_processor = IDProcessor(dict())

        self.assertEqual(IDProcessor.DEFAULT_EXPERIMENT_DESCRIPTION, id_processor.get_experiment_description())

    def test_get_project_description_pass(self):
        json_data = {"project_description": "this is a test description"}
        id_processor = IDProcessor(json_data)

        self.assertEqual("this is a test description", id_processor.get_project_description())

    def test_get_project_description_fail(self):
        json_data = {"project_description": None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_project_description)

    def test_get_project_description_fail_2(self):
        json_data = {"project_description": 1234}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_project_description)

    def test_get_project_description_fail_3(self):
        json_data = {"project_description": {}}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_project_description)

    def test_get_project_name_fail(self):
        json_data = {"project_name": None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_project_name)

    def test_get_project_name_fail_2(self):
        json_data = {"project_name": 12334}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_project_name)

    def test_get_project_name_fail_3(self):
        id_processor = IDProcessor({})
        self.assertIsNone(id_processor.get_project_name(throw_exception=False))

    def test_get_job_id_fail(self):
        json_data = {"job_id": None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_job_id)

    def test_get_job_id_fail_2(self):
        json_data = {"job_id": 12334}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_job_id)

    def test_get_job_id_fail_3(self):
        id_processor = IDProcessor({})
        self.assertIsNone(id_processor.get_job_id(throw_exception=False))

    def test_get_project_id_fail(self):
        json_data = {"project_id": None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_project_id)

    def test_get_project_id_fail_2(self):
        json_data = {"project_id": 12334}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_project_id)

    def test_get_project_id_fail_3(self):
        id_processor = IDProcessor({})
        self.assertIsNone(id_processor.get_project_id(throw_exception=False))

    def test_get_device_id_fail(self):
        json_data = {"device_id": None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_device_id)

    def test_get_device_id_fail_2(self):
        json_data = {"device_id": 12334}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_device_id)

    def test_get_device_id_fail_3(self):
        id_processor = IDProcessor({})
        self.assertIsNone(id_processor.get_device_id(throw_exception=False))

    def test_get_project_name_pass(self):
        json_data = {"project_name": "None"}
        id_processor = IDProcessor(json_data)

        self.assertEqual("None", id_processor.get_project_name())

    def test_get_api_key_pass(self):
        json_data = {"api_key": "None"}
        id_processor = IDProcessor(json_data)

        self.assertEqual("None", id_processor.get_api_key())

    def test_get_api_key_fail_1(self):
        json_data = {"api_key": None}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_api_key)

    def test_get_api_key_fail_2(self):
        json_data = {"api_key": 10}
        id_processor = IDProcessor(json_data)

        self.assertRaises(ValueError, id_processor.get_api_key)

    def test_get_api_key_fail_3(self):
        json_data = {"api_key": None}
        id_processor = IDProcessor(json_data)

        self.assertIsNone(
            id_processor.get_api_key(
                throw_exception=False))
    
    def test_valid_chars_pass(self):
        self.assertTrue(RequestProcessor()._valid_chars("12345jladfvvjdrfvdfjlsjdkflks"))
        self.assertFalse(RequestProcessor()._valid_chars("adfsjdfsdklsfklj;"))
        self.assertFalse(RequestProcessor()._valid_chars("*"))

    def test_get_num_jobs_pass(self):
        self.assertEqual(40, IDProcessor({"num_jobs": 40}).get_num_jobs())
    
    def test_get_num_devices_pass(self):
        self.assertEqual(40, IDProcessor({"num_devices": 40}).get_num_devices())
