from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import JobStatus
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model.termination_criteria import DurationTerminationCriteria
from dependencies.python.fmlaas.utils import get_epoch_time
from .abstract_model_testcase import AbstractModelTestCase


class JobTestCase(AbstractModelTestCase):

    def _build_complex_job(self):
        job = Job("my_id",
                  ["test1", "test2"],
                  JobStatus.COMPLETED.value,
                  {
                      "name": "21313124/123123/123235345",
                      "entity_id": "123235345",
                      "size": "2134235"},
                  {
                      "name": "21313124/123123/123235345",
                      "entity_id": "123235345",
                      "size": "2134234"},
                  {
                      'num_devices': "5",
                      "num_buffer_devices": "0",
                      "device_selection_strategy": "RANDOM",
                      "termination_criteria": []},
                  {
                      "123235345": {
                          "name": "21313124/123123/123235345",
                                  "entity_id": "123235345",
                                  "size": "2134235"}},
                  "December 19th, 2019",
                  "0",
                  "fl_project_12312313",
                  "123121231232131231")

        job_json = {
            'ID': 'my_id',
            'status': 'COMPLETED',
            'devices': [
                'test1',
                'test2'],
            'aggregate_model': {
                "name": "21313124/123123/123235345",
                "entity_id": "123235345",
                "size": "2134235"},
            'start_model': {
                "name": "21313124/123123/123235345",
                "entity_id": "123235345",
                "size": "2134234"},
            'configuration': {
                'num_devices': "5",
                "num_buffer_devices": "0",
                "device_selection_strategy": "RANDOM",
                "termination_criteria": []},
            'models': {
                "123235345": {
                    "name": "21313124/123123/123235345",
                            "entity_id": "123235345",
                            "size": "2134235"}},
            'created_on': 'December 19th, 2019',
            "billable_size": "0",
            "project_id": "fl_project_12312313",
            "job_sequence_id": "123121231232131231"}

        return job, job_json

    def test_to_json_pass(self):
        job, json_data = self._build_complex_job()

        self.assertEqual(json_data, job.to_json())

    def test_from_json_pass(self):
        orig_job, json_data = self._build_complex_job()

        job = Job.from_json(json_data)

        self.assertEqual(orig_job, job)

    def test_add_model_pass(self):
        job = self._build_job(1)

        model = Model("12312312", "2345/device_models/12312312", "234342324")

        job.add_model(model)

        self.assertTrue(model.get_entity_id() in job.models)
        self.assertTrue(
            "12312312" in job.models[model.get_entity_id()]["name"])
        self.assertEqual(model.get_size(),
                         job.models[model.get_entity_id()]["size"])

    def test_get_models(self):
        job, _ = self._build_complex_job()

        models = job.get_models()

        self.assertEqual(len(models), 1)
        self.assertTrue("123235345" in models)

    def test_is_cancelled_pass_1(self):
        job = self._build_job(1)
        job.set_status(JobStatus.CANCELLED)

        self.assertTrue(job.is_cancelled())

    def test_is_cancelled_pass_2(self):
        job = self._build_job(1)
        job.set_status(JobStatus.COMPLETED)

        self.assertFalse(job.is_cancelled())

    def test_is_in_progress_pass_1(self):
        job = self._build_job(1)
        job.set_status(JobStatus.IN_PROGRESS)

        self.assertTrue(job.is_in_progress())

    def test_is_in_progress_pass_2(self):
        job = self._build_job(1)
        job.set_status(JobStatus.AGGREGATION_IN_PROGRESS)

        self.assertFalse(job.is_in_progress())

    def test_is_aggregation_in_progress_pass_1(self):
        job = self._build_job(1)
        job.set_status(JobStatus.AGGREGATION_IN_PROGRESS)

        self.assertTrue(job.is_aggregation_in_progress())

    def test_is_aggregation_in_progress_pass_2(self):
        job = self._build_job(1)
        job.set_status(JobStatus.IN_PROGRESS)

        self.assertFalse(job.is_aggregation_in_progress())

    def test_is_complete_pass_1(self):
        job = self._build_job(1)
        job.set_status(JobStatus.COMPLETED)

        self.assertTrue(job.is_complete())

    def test_is_complete_pass_2(self):
        job = self._build_job(1)
        job.set_status(JobStatus.IN_PROGRESS)

        self.assertFalse(job.is_complete())

    def test_is_active_pass_1(self):
        job = self._build_job(1)
        job.set_status(JobStatus.COMPLETED)

        self.assertFalse(job.is_active())

    def test_is_active_pass_2(self):
        job = self._build_job(1)
        job.set_status(JobStatus.IN_PROGRESS)

        self.assertTrue(job.is_active())

    def test_is_active_pass_3(self):
        job = self._build_job(1)
        job.set_status(JobStatus.AGGREGATION_IN_PROGRESS)

        self.assertTrue(job.is_active())

    def test_contains_device_pass(self):
        job = self._build_job(1)

        self.assertTrue(job.contains_device("123"))
        self.assertFalse(job.contains_device("test10"))
        self.assertTrue(job.contains_device("234"))

    def test_is_device_active_pass(self):
        job = self._build_job(1)

        job.set_start_model(
            Model(
                "34234342",
                "34234342/start_model",
                "234514"))

        self.assertTrue(job.is_device_active("123"))
        self.assertTrue(job.is_device_active("234"))

        job.add_model(Model("123", "34234342/device_models/123", "12355"))

        self.assertFalse(job.is_device_active("123"))
        self.assertTrue(job.is_device_active("234"))

    def test_is_device_active_pass_2(self):
        job = self._build_job(1)
        job.set_status(JobStatus.COMPLETED)

        self.assertFalse(job.is_device_active("123"))
        self.assertFalse(job.is_device_active("234"))

    def test_is_aggregate_model_set_pass_1(self):
        job = self._build_job(1)

        self.assertFalse(job.is_aggregate_model_set())

    def test_is_aggregate_model_set_pass_2(self):
        job = self._build_job(1)

        job.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))

        self.assertTrue(job.is_aggregate_model_set())

    def test_is_ready_for_aggregation_pass(self):
        job = self._build_job(1)

        self.assertFalse(job.is_ready_for_aggregation())
        self.assertEqual(job.get_status(), JobStatus.INITIALIZED)

    def test_is_in_initialization_pass_1(self):
        job = self._build_job(1)

        self.assertTrue(job.is_in_initialization())
        self.assertEqual(job.get_status(), JobStatus.INITIALIZED)

    def test_is_in_initialization_pass_2(self):
        job = self._build_job(1)

        job.set_start_model(Model("1234", "1234/start_model", "1234345"))

        self.assertFalse(job.is_in_initialization())
        self.assertEqual(job.get_status(), JobStatus.IN_PROGRESS)

    def test_set_start_model_pass_1(self):
        job = self._build_job(1)

        start_model = Model("1234", "1234/start_model", "1234345")
        job.set_start_model(start_model)

        self.assertEqual(
            start_model.to_json(),
            job.get_start_model().to_json())
        self.assertEqual(job.get_status(), JobStatus.IN_PROGRESS)

    def test_set_start_model_pass_2(self):
        job = self._build_job(1)

        start_model = Model("1234", "1234/start_model", "1234345")
        job.set_start_model(start_model)
        job.set_start_model(
            Model(
                "123445645",
                "123445645/start_model",
                "6435453"))

        self.assertEqual(
            start_model.to_json(),
            job.get_start_model().to_json())
        self.assertEqual(job.get_status(), JobStatus.IN_PROGRESS)

    def test_is_ready_for_aggregation_pass_2(self):
        job = self._build_job(1)

        job.add_model(Model("123", "fdldasf", "1231231"))
        job.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(job.is_ready_for_aggregation())

    def test_should_aggregate_pass(self):
        job = self._build_job(1)

        self.assertFalse(job.should_aggregate())
        self.assertEqual(job.get_status(), JobStatus.INITIALIZED)

    def test_should_aggregate_pass_2(self):
        job = self._build_job(1)

        job.set_start_model(Model("123456", "123456/start_model", "12321"))
        job.add_model(Model("123", "fdldasf", "1231231"))
        job.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(job.should_aggregate())
        self.assertEqual(job.get_status(), JobStatus.IN_PROGRESS)

    def test_should_aggregate_pass_3(self):
        job = self._build_job(1)

        job.add_model(Model("123", "fdldasf", "1231231"))
        job.add_model(Model("234", "fdldasf", "1231231"))
        job.set_status(JobStatus.COMPLETED)

        self.assertFalse(job.should_aggregate())

    def test_is_device_model_submitted_pass(self):
        job = self._build_job(1)

        self.assertFalse(job.is_device_model_submitted("123"))
        self.assertFalse(job.is_device_model_submitted("234"))

        job.add_model(Model("123", "fdldasf", "1231231"))

        self.assertTrue(job.is_device_model_submitted("123"))
        self.assertFalse(job.is_device_model_submitted("234"))

        job.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(job.is_device_model_submitted("123"))
        self.assertTrue(job.is_device_model_submitted("234"))

    def test_cancel_pass(self):
        job = self._build_job(1)

        job.set_start_model(Model("1234", "1234/start_model", "231241"))

        self.assertEqual(job.get_status(), JobStatus.IN_PROGRESS)

        job.cancel()

        self.assertEqual(job.get_status(), JobStatus.CANCELLED)
        self.assertEqual(
            job.get_start_model().to_json(),
            job.get_end_model().to_json())
        self.assertEqual(job.get_billable_size(), 231241)

    def test_cancel_pass_2(self):
        job = self._build_job(1)

        job.cancel()

        self.assertEqual(job.get_status(), JobStatus.CANCELLED)
        self.assertEqual(job.get_billable_size(), 0)

    def test_complete_pass(self):
        job = self._build_job(1)

        job.set_start_model(Model("1234", "1234/start_model", "231241"))

        job.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))
        job.complete()

        self.assertEqual(job.get_status(), JobStatus.COMPLETED)
        self.assertEqual(
            job.get_aggregate_model().to_json(),
            job.get_end_model().to_json())
        self.assertEqual(job.get_billable_size(), 243565)

    def test_calculate_billable_size_pass_1(self):
        job = self._build_job(1)

        job.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))

        self.assertEqual(job.calculate_billable_size(), "12324")

    def test_calculate_billable_size_pass_2(self):
        job = self._build_job(1)

        job.add_model(Model("1231241241", "123/345/1231241241", "55543"))
        job.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))

        self.assertEqual(job.calculate_billable_size(), "67867")

    def test_should_terminate_pass(self):
        job = self._build_job(1)
        config = job.get_configuration()
        config.add_termination_criteria(DurationTerminationCriteria(0, 2313123.1231))
        job.set_configuration(config)

        self.assertTrue(job.should_terminate())

    def test_should_terminate_pass_2(self):
        job = self._build_job(1)
        config = job.get_configuration()
        config.add_termination_criteria(DurationTerminationCriteria(10, float(get_epoch_time())))
        job.set_configuration(config)

        self.assertFalse(job.should_terminate())

    def test_reset_termination_criteria_pass(self):
        job = self._build_job(1)
        config = job.get_configuration()
        config.add_termination_criteria(DurationTerminationCriteria(10, float(get_epoch_time()) - 100))
        job.set_configuration(config)

        self.assertTrue(job.should_terminate())

        job.reset_termination_criteria()

        self.assertFalse(job.should_terminate())

    def test_equals_pass(self):
        job_1 = self._build_job(1)
        job_2 = self._build_job(1)
        job_3, _ = self._build_complex_job()

        self.assertFalse(job_1 == job_3)
        self.assertFalse(job_2 == job_3)
        self.assertTrue(job_1 == job_2)
