import unittest

from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import JobStatus
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model.termination_criteria import DurationTerminationCriteria
from dependencies.python.fmlaas.utils import get_epoch_time

class JobTestCase(unittest.TestCase):

    def _build_default_job(self):
        builder = JobBuilder()
        builder.set_id("test_id")
        builder.set_parent_project_id("fl_project_1232234")
        builder.set_devices(["123", "234"])
        configuration = JobConfiguration(2, 0, "RANDOM", [])
        builder.set_configuration(configuration.to_json())

        return builder.build()

    def test_to_json_pass(self):
        job = Job("my_id",
            ["test1", "test2"],
            JobStatus.COMPLETED.value,
            {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"},
            {"name" : "21313124/21313124", "entity_id" : "21313124", "size" : "21313124"},
            {"config info" : "here"},
            {"test1" : {"size" : "123300"}},
            "December 19th, 2019",
            "1234345",
            "fl_project_12312313")

        job_json = job.to_json()

        self.assertEqual("my_id", job_json["ID"])
        self.assertEqual("COMPLETED", job_json["status"])
        self.assertEqual(["test1", "test2"], job_json["devices"])
        self.assertEqual({"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"}, job_json["aggregate_model"])
        self.assertEqual({"name" : "21313124/21313124", "entity_id" : "21313124", "size" : "21313124"}, job_json["start_model"])
        self.assertEqual({"config info" : "here"}, job_json["configuration"])
        self.assertEqual({"test1" : {"size" : "123300"}}, job_json["models"])
        self.assertEqual("December 19th, 2019", job_json["created_on"])
        self.assertEqual("1234345", job_json["billable_size"])
        self.assertEqual("fl_project_12312313", job_json["parent_project_id"])

    def test_from_json_pass(self):
        job_json = {'ID': 'my_id', 'status': 'COMPLETED', 'devices': ['test1', 'test2'], 'aggregate_model': {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"}, 'start_model': {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"}, 'configuration': {'num_devices' : "5", "num_buffer_devices" : "0", "device_selection_strategy" : "RANDOM", "termination_criteria" : []}, 'models': {"123235345" : {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"}}, 'created_on': 'December 19th, 2019', "billable_size" : "0", "parent_project_id" : "fl_project_12312313"}

        job = Job.from_json(job_json)

        self.assertEqual(job.get_id(), job_json["ID"])
        self.assertEqual(job.get_status(), JobStatus.COMPLETED)
        self.assertEqual(job.get_devices(), job_json["devices"])
        self.assertEqual(job.get_aggregate_model().to_json(), job_json["aggregate_model"])
        self.assertEqual(job.get_configuration().to_json(), job_json["configuration"])
        self.assertEqual(job.get_models()["123235345"].to_json(), job_json["models"]["123235345"])
        self.assertEqual(job.get_created_on(), job_json["created_on"])
        self.assertEqual(job.get_start_model().to_json(), job_json["start_model"])
        self.assertEqual(job.get_billable_size(), int(job_json["billable_size"]))
        self.assertEqual(job.get_parent_project_id(), job_json["parent_project_id"])

    def test_add_model_pass(self):
        job = self._build_default_job()

        model = Model("12312312", "2345/device_models/12312312", "234342324")

        job.add_model(model)

        self.assertTrue(model.get_entity_id() in job.models)
        self.assertTrue("12312312" in job.models[model.get_entity_id()]["name"])
        self.assertEqual(model.get_size(), job.models[model.get_entity_id()]["size"])

    def test_get_models(self):
        job = Job("my_id",
            ["test1", "test2"],
            JobStatus.COMPLETED,
            {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"},
            {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"},
            {"config info" : "here"},
            {"123235345" : {"name" : "21313124/123123/123235345", "entity_id" : "123235345", "size" : "2134235"}, "1232353465" : {"name" : "21313124/123123/1232353465", "entity_id" : "1232353465", "size" : "2134235"}},
            "December 19th, 2019",
            "0",
            "fl_project_12312313")

        models = job.get_models()

        self.assertEqual(len(models), 2)
        self.assertTrue("123235345" in models)
        self.assertTrue("1232353465" in models)

    def test_is_cancelled_pass_1(self):
        job = self._build_default_job()
        job.set_status(JobStatus.CANCELLED)

        self.assertTrue(job.is_cancelled())

    def test_is_cancelled_pass_2(self):
        job = self._build_default_job()
        job.set_status(JobStatus.COMPLETED)

        self.assertFalse(job.is_cancelled())

    def test_is_in_progress_pass_1(self):
        job = self._build_default_job()
        job.set_status(JobStatus.IN_PROGRESS)

        self.assertTrue(job.is_in_progress())

    def test_is_in_progress_pass_2(self):
        job = self._build_default_job()
        job.set_status(JobStatus.AGGREGATION_IN_PROGRESS)

        self.assertFalse(job.is_in_progress())

    def test_is_aggregation_in_progress_pass_1(self):
        job = self._build_default_job()
        job.set_status(JobStatus.AGGREGATION_IN_PROGRESS)

        self.assertTrue(job.is_aggregation_in_progress())

    def test_is_aggregation_in_progress_pass_2(self):
        job = self._build_default_job()
        job.set_status(JobStatus.IN_PROGRESS)

        self.assertFalse(job.is_aggregation_in_progress())

    def test_is_complete_pass_1(self):
        job = self._build_default_job()
        job.set_status(JobStatus.COMPLETED)

        self.assertTrue(job.is_complete())

    def test_is_complete_pass_2(self):
        job = self._build_default_job()
        job.set_status(JobStatus.IN_PROGRESS)

        self.assertFalse(job.is_complete())

    def test_is_active_pass_1(self):
        job = self._build_default_job()
        job.set_status(JobStatus.COMPLETED)

        self.assertFalse(job.is_active())

    def test_is_active_pass_2(self):
        job = self._build_default_job()
        job.set_status(JobStatus.IN_PROGRESS)

        self.assertTrue(job.is_active())

    def test_is_active_pass_3(self):
        job = self._build_default_job()
        job.set_status(JobStatus.AGGREGATION_IN_PROGRESS)

        self.assertTrue(job.is_active())

    def test_contains_device_pass(self):
        job = self._build_default_job()

        self.assertTrue(job.contains_device("123"))
        self.assertFalse(job.contains_device("test10"))
        self.assertTrue(job.contains_device("234"))

    def test_is_device_active_pass(self):
        job = self._build_default_job()

        job.set_start_model(Model("34234342", "34234342/start_model", "234514"))

        self.assertTrue(job.is_device_active("123"))
        self.assertTrue(job.is_device_active("234"))

        job.add_model(Model("123", "34234342/device_models/123", "12355"))

        self.assertFalse(job.is_device_active("123"))
        self.assertTrue(job.is_device_active("234"))

    def test_is_device_active_pass_2(self):
        job = self._build_default_job()
        job.set_status(JobStatus.COMPLETED)

        self.assertFalse(job.is_device_active("123"))
        self.assertFalse(job.is_device_active("234"))

    def test_is_aggregate_model_set_pass_1(self):
        job = self._build_default_job()

        self.assertFalse(job.is_aggregate_model_set())

    def test_is_aggregate_model_set_pass_2(self):
        job = self._build_default_job()

        job.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))

        self.assertTrue(job.is_aggregate_model_set())

    def test_is_ready_for_aggregation_pass(self):
        job = self._build_default_job()

        self.assertFalse(job.is_ready_for_aggregation())
        self.assertEqual(job.get_status(), JobStatus.INITIALIZED)

    def test_is_in_initialization_pass_1(self):
        job = self._build_default_job()

        self.assertTrue(job.is_in_initialization())
        self.assertEqual(job.get_status(), JobStatus.INITIALIZED)

    def test_is_in_initialization_pass_2(self):
        job = self._build_default_job()

        job.set_start_model(Model("1234", "1234/start_model", "1234345"))

        self.assertFalse(job.is_in_initialization())
        self.assertEqual(job.get_status(), JobStatus.IN_PROGRESS)

    def test_set_start_model_pass_1(self):
        job = self._build_default_job()

        start_model = Model("1234", "1234/start_model", "1234345")
        job.set_start_model(start_model)

        self.assertEqual(start_model.to_json(), job.get_start_model().to_json())
        self.assertEqual(job.get_status(), JobStatus.IN_PROGRESS)

    def test_set_start_model_pass_2(self):
        job = self._build_default_job()

        start_model = Model("1234", "1234/start_model", "1234345")
        job.set_start_model(start_model)
        job.set_start_model(Model("123445645", "123445645/start_model", "6435453"))

        self.assertEqual(start_model.to_json(), job.get_start_model().to_json())
        self.assertEqual(job.get_status(), JobStatus.IN_PROGRESS)

    def test_is_ready_for_aggregation_pass_2(self):
        job = self._build_default_job()

        job.add_model(Model("123", "fdldasf", "1231231"))
        job.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(job.is_ready_for_aggregation())

    def test_should_aggregate_pass(self):
        job = self._build_default_job()

        self.assertFalse(job.should_aggregate())
        self.assertEqual(job.get_status(), JobStatus.INITIALIZED)

    def test_should_aggregate_pass_2(self):
        job = self._build_default_job()

        job.set_start_model(Model("123456", "123456/start_model", "12321"))
        job.add_model(Model("123", "fdldasf", "1231231"))
        job.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(job.should_aggregate())
        self.assertEqual(job.get_status(), JobStatus.IN_PROGRESS)

    def test_should_aggregate_pass_3(self):
        job = self._build_default_job()

        job.add_model(Model("123", "fdldasf", "1231231"))
        job.add_model(Model("234", "fdldasf", "1231231"))
        job.set_status(JobStatus.COMPLETED)

        self.assertFalse(job.should_aggregate())

    def test_is_device_model_submitted_pass(self):
        job = self._build_default_job()

        self.assertFalse(job.is_device_model_submitted("123"))
        self.assertFalse(job.is_device_model_submitted("234"))

        job.add_model(Model("123", "fdldasf", "1231231"))

        self.assertTrue(job.is_device_model_submitted("123"))
        self.assertFalse(job.is_device_model_submitted("234"))

        job.add_model(Model("234", "fdldasf", "1231231"))

        self.assertTrue(job.is_device_model_submitted("123"))
        self.assertTrue(job.is_device_model_submitted("234"))

    def test_cancel_pass(self):
        job = self._build_default_job()

        job.set_start_model(Model("1234", "1234/start_model", "231241"))

        self.assertEqual(job.get_status(), JobStatus.IN_PROGRESS)

        job.cancel()

        self.assertEqual(job.get_status(), JobStatus.CANCELLED)
        self.assertEqual(job.get_start_model().to_json(), job.get_end_model().to_json())
        self.assertEqual(job.get_billable_size(), 231241)

    def test_cancel_pass_2(self):
        job = self._build_default_job()

        job.cancel()

        self.assertEqual(job.get_status(), JobStatus.CANCELLED)
        self.assertEqual(job.get_billable_size(), 0)

    def test_complete_pass(self):
        job = self._build_default_job()

        job.set_start_model(Model("1234", "1234/start_model", "231241"))

        job.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))
        job.complete()

        self.assertEqual(job.get_status(), JobStatus.COMPLETED)
        self.assertEqual(job.get_aggregate_model().to_json(), job.get_end_model().to_json())
        self.assertEqual(job.get_billable_size(), 243565)

    def test_calculate_billable_size_pass_1(self):
        builder = JobBuilder()
        builder.set_id("test_id")
        builder.set_parent_project_id("fl_project_1232234")
        builder.set_devices(["123", "234"])
        configuration = JobConfiguration(50, 0, "RANDOM", [])
        builder.set_configuration(configuration.to_json())
        job = builder.build()

        job.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))

        self.assertEqual(job.calculate_billable_size(), "12324")

    def test_calculate_billable_size_pass_2(self):
        job = self._build_default_job()

        job.add_model(Model("1231241241", "123/345/1231241241", "55543"))
        job.set_aggregate_model(Model("sefsljkdf", "123123", "12324"))

        self.assertEqual(job.calculate_billable_size(), "67867")

    def test_should_terminate_pass(self):
        builder = JobBuilder()
        builder.set_id("test_id")
        builder.set_parent_project_id("fl_project_1232234")
        builder.set_devices(["123", "234"])
        configuration = JobConfiguration(50, 0, "RANDOM", [
            DurationTerminationCriteria(0, 2313123.1231).to_json()
        ])
        builder.set_configuration(configuration.to_json())
        job = builder.build()

        self.assertTrue(job.should_terminate())

    def test_should_terminate_pass_2(self):
        builder = JobBuilder()
        builder.set_id("test_id")
        builder.set_parent_project_id("fl_project_1232234")
        builder.set_devices(["123", "234"])
        configuration = JobConfiguration(50, 0, "RANDOM", [
            DurationTerminationCriteria(10, float(get_epoch_time())).to_json()
        ])
        builder.set_configuration(configuration.to_json())
        job = builder.build()

        self.assertFalse(job.should_terminate())

    def test_reset_termination_criteria_pass(self):
        builder = JobBuilder()
        builder.set_id("test_id")
        builder.set_parent_project_id("fl_project_1232234")
        builder.set_devices(["123", "234"])
        configuration = JobConfiguration(50, 0, "RANDOM", [
            DurationTerminationCriteria(10, float(get_epoch_time()) - 100).to_json()
        ])
        builder.set_configuration(configuration.to_json())
        job = builder.build()

        self.assertTrue(job.should_terminate())

        job.reset_termination_criteria()

        self.assertFalse(job.should_terminate())
