from dependencies.python.fmlaas.controller.model_uploaded import (
    get_model_process_function, handle_device_model_update,
    handle_experiment_start_model, handle_job_aggregate_model)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import (DBObject, Job, JobConfiguration,
                                              Model, Project)

from ..abstract_testcase import AbstractTestCase


class ModelUploadedControllerTestCase(AbstractTestCase):

    def test_get_model_process_function_pass_1(self):
        model = Model("1232344", "project_id/experiment_id/job_id/device_models/1232344", "923843287")

        self.assertEqual(
            handle_device_model_update,
            get_model_process_function(str(model.name)))

    def test_get_model_process_function_pass_2(self):
        model = Model("1234", "project_id/experiment_id/job_id/aggregate_model", "923843287")

        self.assertEqual(
            handle_job_aggregate_model,
            get_model_process_function(
                model.name))

    def test_get_model_process_function_pass_3(self):
        model = Model("1234", "project_id/experiment_id/start_model", "923843287")

        self.assertEqual(
            handle_experiment_start_model,
            get_model_process_function(
                model.name))

    def test_handle_device_model_update_pass(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "project_id/experiment_id/1234/device_models/1232344", "1232131")

        job = self._build_simple_job()
        job._aggregate_model = {}
        job.save_to_db(db_)

        self.assertFalse(job.is_device_model_submitted("1232344"))

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertTrue(should_aggregate)

        job_2 = DBObject.load_from_db(Job, job.id, db_)

        self.assertTrue(job_2.is_device_model_submitted("1232344"))

    def test_handle_device_model_update_pass_no_aggregation(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "project_id/experiment_id/1234/device_models/1232344", "1232131")

        job = self._build_simple_job()
        job.configuration = JobConfiguration(2, 0, "RANDOM", []).to_json()
        job._aggregate_model = {}
        job.devices = ["1232344", "4567"]
        job.save_to_db(db_)

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertFalse(should_aggregate)
        self.assertTrue(job.is_in_progress())
        self.assertFalse(job.is_ready_for_aggregation())

    def test_handle_device_model_update_duplicate_pass(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "project_id/experiment_id/1234/device_models/3456", "1232131")
        model_2 = Model(None, "project_id/experiment_id/1234/device_models/3456", "66665")

        job = self._build_simple_job()
        job.save_to_db(db_)

        handle_device_model_update(model, None, db_)
        handle_device_model_update(model_2, None, db_)

        job_2 = DBObject.load_from_db(Job, job.id, db_)
        self.assertTrue(job_2.is_device_model_submitted("3456"))
        self.assertEqual("66665", job_2.models["3456"]["size"])

    def test_handle_device_model_update_pass_agg_in_progress(self):
        db_ = InMemoryDBInterface()
        model = Model(None, "project_id/experiment_id/1234/device_models/3456", "1232131")

        job = self._build_simple_job()
        job._aggregate_model = {}
        job.save_to_db(db_)

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertTrue(should_aggregate)

        should_aggregate = handle_device_model_update(model, None, db_)
        self.assertFalse(should_aggregate)

    def test_handle_job_aggregate_model_pass(self):
        project_db = InMemoryDBInterface()
        db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job._aggregate_model = {}
        job.save_to_db(db_)

        project = self._build_simple_project()

        experiment = self._build_simple_experiment()
        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        model = Model(None, "project_id/experiment_id/1234/device_models/3456", "1232131")
        handle_device_model_update(model, None, db_)

        aggregate_model = Model(None, "project_id/experiment_id/1234/aggregate_model", "435345")
        should_aggregate = handle_job_aggregate_model(
            aggregate_model, project_db, db_)
        self.assertFalse(should_aggregate)

        job_2 = DBObject.load_from_db(Job, job.id, db_)

        self.assertTrue(job_2.is_complete())
        self.assertEqual(job_2.aggregate_model.size, "435345")

    def test_handle_job_aggregate_model_pass_2(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job._aggregate_model = {}
        job.save_to_db(job_db)

        job_2 = self._build_simple_job()
        job_2._aggregate_model = {}
        job_2._id = "test_job_2"
        job_2.save_to_db(job_db)

        project = self._build_simple_project()

        experiment = self._build_simple_experiment()
        experiment.current_model = Model("1234",
                                         "1234/start_model",
                                         "123211")

        experiment.add_job(job)
        experiment.add_job(job_2)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        model = Model(None, "project_id/experiment_id/1234/device_models/3456", "1232131")
        handle_device_model_update(model, None, job_db)
        aggregate_model = Model(None, "project_id/experiment_id/1234/aggregate_model", "435345")
        handle_job_aggregate_model(aggregate_model, project_db, job_db)

        project_from_db = DBObject.load_from_db(
            Project, project.id, project_db)
        self.assertEqual(1, len(project_from_db.get_active_jobs()))
        self.assertEqual(
            job_2.id,
            project_from_db.get_active_jobs()[0])

        job_2_from_db = DBObject.load_from_db(Job, job_2.id, job_db)
        job_from_db = DBObject.load_from_db(Job, job.id, job_db)
        self.assertEqual(
            job_from_db.aggregate_model,
            job_2_from_db.start_model)

    def test_handle_job_aggregate_model_pass_3(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job._aggregate_model = {}
        job.save_to_db(job_db)

        job_2 = self._build_simple_job()
        job_2._aggregate_model = {}
        job_2._id = "12341"
        job_2.cancel()
        job_2.save_to_db()

        job_3 = self._build_simple_job()
        job_3._aggregate_model = {}
        job_3._id = "12342"
        job_3.save_to_db(job_db)

        project = self._build_simple_project()
        experiment = self._build_simple_experiment()

        experiment.add_job(job)
        experiment.add_job(job_2)
        experiment.add_job(job_3)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        model = Model(None, "project_id/experiment_id/1234/device_models/3456", "1232131")
        handle_device_model_update(model, None, job_db)
        aggregate_model = Model(None, "project_id/experiment_id/1234/aggregate_model", "435345")
        handle_job_aggregate_model(aggregate_model, project_db, job_db)

        project_from_db = DBObject.load_from_db(
            Project, project.id, project_db)
        self.assertEqual(1, len(project_from_db.get_active_jobs()))
        self.assertEqual(
            job_3.id,
            project_from_db.get_active_jobs()[0])

        job_3_from_db = DBObject.load_from_db(Job, job_3.id, job_db)
        job_from_db = DBObject.load_from_db(Job, job.id, job_db)
        self.assertEqual(
            job_from_db.aggregate_model.to_json(),
            job_3_from_db.start_model.to_json())

    def test_handle_experiment_start_model_pass(self):
        project_db = InMemoryDBInterface()
        db_ = InMemoryDBInterface()

        experiment = self._build_simple_experiment()

        project = self._build_simple_project()
        project.add_or_update_experiment(experiment)
        project.save_to_db(project_db)

        model = Model(None, "test_id/experiment_1/start_model", "1232131")
        should_aggregate = handle_experiment_start_model(model, project_db, db_)

        self.assertFalse(should_aggregate)

        loaded_project = DBObject.load_from_db(Project, project.id, project_db)

        self.assertTrue(loaded_project.get_experiment(experiment.id).is_start_model_set())
