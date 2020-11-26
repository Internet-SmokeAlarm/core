from dependencies.python.fmlaas.model import Job, Model, Status, TestingReport
from dependencies.python.fmlaas.model.termination_criteria import \
    DurationTerminationCriteria
from dependencies.python.fmlaas.utils import get_epoch_time

from .abstract_model_testcase import AbstractModelTestCase


class JobTestCase(AbstractModelTestCase):

    def test_to_json_pass(self):
        job, json_data = self._create_job("1")

        self.assertEqual(json_data, job.to_json())

    def test_from_json_pass(self):
        orig_job, json_data = self._create_job("1")

        job = Job.from_json(json_data)

        self.assertEqual(orig_job, job)

    def test_get_add_model_pass(self):
        job, _ = self._create_job("1")

        model = Model("123", "2345/device_models/123", 234342324)
        job.add_model(model)

        self.assertTrue(model.entity_id in job.models)
        self.assertEqual(model, job.models[model.entity_id])

    def test_is_cancelled_pass_1(self):
        job, _ = self._create_job("1")
        job.status = Status.CANCELLED

        self.assertTrue(job.is_cancelled())

    def test_is_cancelled_pass_2(self):
        job, _ = self._create_job("1")
        job.status = Status.COMPLETED

        self.assertFalse(job.is_cancelled())

    def test_is_in_progress_pass_1(self):
        job, _ = self._create_job("1")
        job.status = Status.IN_PROGRESS

        self.assertTrue(job.is_in_progress())

    def test_is_in_progress_pass_2(self):
        job, _ = self._create_job("1")
        job.status = Status.AGGREGATION_IN_PROGRESS

        self.assertFalse(job.is_in_progress())

    def test_is_aggregation_in_progress_pass_1(self):
        job, _ = self._create_job("1")
        job.status = Status.AGGREGATION_IN_PROGRESS

        self.assertTrue(job.is_aggregation_in_progress())

    def test_is_aggregation_in_progress_pass_2(self):
        job, _ = self._create_job("1")
        job.status = Status.IN_PROGRESS

        self.assertFalse(job.is_aggregation_in_progress())

    def test_is_complete_pass_1(self):
        job, _ = self._create_job("1")
        job.status = Status.COMPLETED

        self.assertTrue(job.is_complete())

    def test_is_complete_pass_2(self):
        job, _ = self._create_job("1")
        job.status = Status.IN_PROGRESS

        self.assertFalse(job.is_complete())

    def test_is_active_pass_1(self):
        job, _ = self._create_job("1")
        job.status = Status.COMPLETED

        self.assertFalse(job.is_active())

    def test_is_active_pass_2(self):
        job, _ = self._create_job("1")
        job.status = Status.IN_PROGRESS

        self.assertTrue(job.is_active())

    def test_is_active_pass_3(self):
        job, _ = self._create_job("1")
        job.status = Status.AGGREGATION_IN_PROGRESS

        self.assertTrue(job.is_active())

    def test_contains_device_pass(self):
        job, _ = self._create_job("1")

        self.assertTrue(job.contains_device("123"))
        self.assertFalse(job.contains_device("test10"))

    def test_is_device_active_pass(self):
        job, _ = self._create_job("1")
        model, _ = self._create_model()
        job.start_model = model

        self.assertTrue(job.is_device_active("123"))
        self.assertTrue(job.is_device_active("234"))

        job.add_model(Model("123", "34234342/device_models/123", "12355"))

        self.assertFalse(job.is_device_active("123"))
        self.assertTrue(job.is_device_active("234"))

    def test_is_device_active_pass_2(self):
        job, _ = self._create_job("1")
        job.status = Status.COMPLETED

        self.assertFalse(job.is_device_active("123"))
        self.assertFalse(job.is_device_active("234"))

    def test_is_aggregate_model_set_pass_1(self):
        job, _ = self._create_job("1")

        self.assertFalse(job.is_aggregate_model_set())

    def test_is_aggregate_model_set_pass_2(self):
        job, _ = self._create_job("1")

        job.aggregate_model = Model("sefsljkdf", "123123", "12324")

        self.assertTrue(job.is_aggregate_model_set())

    def test_is_ready_for_aggregation_pass(self):
        job, _ = self._create_job("1")

        self.assertFalse(job.is_ready_for_aggregation())
        self.assertEqual(job.status, Status.INITIALIZED)

    def test_is_in_initialization_pass_1(self):
        job, _ = self._create_job("1")

        self.assertTrue(job.is_in_initialization())
        self.assertEqual(job.status, Status.INITIALIZED)

    def test_is_in_initialization_pass_2(self):
        job, _ = self._create_job("1")

        job.start_model = Model("1234", "1234/start_model", "1234345")

        self.assertFalse(job.is_in_initialization())
        self.assertEqual(job.status, Status.IN_PROGRESS)

    def test_set_start_model_pass_1(self):
        job, _ = self._create_job("1")

        start_model = Model("1234", "1234/start_model", "1234345")
        job.start_model = start_model

        self.assertEqual(
            start_model.to_json(),
            job.start_model.to_json())
        self.assertEqual(job.status, Status.IN_PROGRESS)

    def test_is_ready_for_aggregation_pass_2(self):
        job, _ = self._create_job("1")

        job.add_model(Model("123", "fdldasf", "1231231"))
        job.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(job.is_ready_for_aggregation())

    def test_should_aggregate_pass(self):
        job, _ = self._create_job("1")

        self.assertFalse(job.should_aggregate())
        self.assertEqual(job.status, Status.INITIALIZED)

    def test_should_aggregate_pass_2(self):
        job, _ = self._create_job("1")

        job.start_model = Model("123456", "123456/start_model", "12321")
        job.add_model(Model("123", "fdldasf", "1231231"))
        job.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(job.should_aggregate())
        self.assertEqual(job.status, Status.IN_PROGRESS)

    def test_should_aggregate_pass_3(self):
        job, _ = self._create_job("1")

        job.add_model(Model("123", "fdldasf", "1231231"))
        job.add_model(Model("234", "fdldasf", "1231231"))
        job.status = Status.COMPLETED

        self.assertFalse(job.should_aggregate())

    def test_is_device_model_submitted_pass(self):
        job, _ = self._create_job("1")

        self.assertFalse(job.is_device_model_submitted("123"))
        self.assertFalse(job.is_device_model_submitted("234"))

        job.add_model(Model("123", "fdldasf", "1231231"))

        self.assertTrue(job.is_device_model_submitted("123"))
        self.assertFalse(job.is_device_model_submitted("234"))

        job.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(job.is_device_model_submitted("123"))
        self.assertTrue(job.is_device_model_submitted("234"))

    def test_cancel_pass(self):
        job, _ = self._create_job("1")

        job.start_model = Model("1234", "1234/start_model", 231241)

        self.assertEqual(job.status, Status.IN_PROGRESS)

        job.cancel()

        self.assertEqual(job.status, Status.CANCELLED)
        self.assertEqual(
            job.start_model.to_json(),
            job.end_model.to_json())
        self.assertEqual(job.billable_size, 231241)

    def test_cancel_pass_2(self):
        job, _ = self._create_job("1")

        job.cancel()

        self.assertEqual(job.status, Status.CANCELLED)
        self.assertEqual(job.billable_size, 0)

    def test_complete_pass(self):
        job, _ = self._create_job("1")

        job.start_model = Model("1234", "1234/start_model", "231241")
        job.aggregate_model = Model("sefsljkdf", "123123", "12324")

        job.complete()

        self.assertEqual(job.status, Status.COMPLETED)
        self.assertEqual(
            job.aggregate_model.to_json(),
            job.end_model.to_json())
        self.assertEqual(job.billable_size, 243565)

    def test_calculate_billable_size_pass_1(self):
        job, _ = self._create_job("1")

        job.aggregate_model = Model("sefsljkdf", "123123", "12324")

        self.assertEqual(job.calculate_billable_size(), 12324)

    def test_calculate_billable_size_pass_2(self):
        job, _ = self._create_job("1")

        job.add_model(Model("1231241241", "123/345/1231241241", "55543"))
        job.aggregate_model = Model("sefsljkdf", "123123", "12324")

        self.assertEqual(job.calculate_billable_size(), 67867)

    def test_should_terminate_pass(self):
        job, _ = self._create_job("1")
        config = job.configuration
        config.add_termination_criteria(DurationTerminationCriteria(0, 2313123))
        job._configuration = config

        self.assertTrue(job.should_terminate())

    def test_should_terminate_pass_2(self):
        job, _ = self._create_job("1")
        config = job.configuration
        config.add_termination_criteria(DurationTerminationCriteria(10, get_epoch_time()))
        job._configuration = config

        self.assertFalse(job.should_terminate())

    def test_reset_termination_criteria_pass(self):
        job, _ = self._create_job("1")
        config = job.configuration
        config.add_termination_criteria(DurationTerminationCriteria(10, get_epoch_time() - 100))
        job._configuration = config

        self.assertTrue(job.should_terminate())

        job.reset_termination_criteria()

        self.assertFalse(job.should_terminate())

    def test_equals_pass(self):
        job_1, _ = self._create_job("1")
        job_2, _ = self._create_job("1")
        job_3, _ = self._create_job("3")

        self.assertFalse(job_1 == job_3)
        self.assertFalse(job_2 == job_3)
        self.assertTrue(job_1 == job_2)

    def test_add_testing_report_pass(self):
        job, _ = self._create_job("1")
        testing_report = TestingReport([[10, 0, 0], [0, 10, 0], [0, 0, 10]], 88.44, 2.454, "12124325adfdsfa2radfads234r")

        job.add_testing_report(testing_report)

        self.assertTrue("12124325adfdsfa2radfads234r" in job.testing_reports)
