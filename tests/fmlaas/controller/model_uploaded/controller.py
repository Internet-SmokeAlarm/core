from dependencies.python.fmlaas.controller.model_uploaded import (
    get_model_process_function, handle_device_model_update,
    handle_experiment_start_model, handle_job_aggregate_model)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import DBObject, Model, Project

from ..abstract_testcase import AbstractTestCase


class ModelUploadedControllerTestCase(AbstractTestCase):

    def test_get_model_process_function_pass_1(self):
        model = Model("1232344", "project_id/experiment_id/job_id/device_models/1232344", 923843287)

        self.assertEqual(
            handle_device_model_update,
            get_model_process_function(str(model.name)))

    def test_get_model_process_function_pass_2(self):
        model = Model("1234", "project_id/experiment_id/job_id/aggregate_model", 923843287)

        self.assertEqual(
            handle_job_aggregate_model,
            get_model_process_function(str(model.name)))

    def test_get_model_process_function_pass_3(self):
        model = Model("1234", "project_id/experiment_id/start_model", 923843287)

        self.assertEqual(
            handle_experiment_start_model,
            get_model_process_function(str(model.name)))

    def test_handle_device_model_update_pass(self):
        project_db = InMemoryDBInterface()

        job = self._build_simple_job("1")

        project = self._build_simple_project()
        experiment, _ = self._build_simple_experiment("1")

        experiment.add_or_update_job(job)

        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        model = Model(None, f"{project.id}/{experiment.id}/{job.id}/device_models/12344", 1232131)
        handle_device_model_update(model, project_db)

        project_from_db = DBObject.load_from_db(
            Project, project.id, project_db)
        
        experiment_from_db = project_from_db.get_experiment(experiment.id)
        job_from_db = experiment_from_db.get_job(job.id)

        self.assertTrue(job_from_db.is_aggregation_in_progress())

    def test_handle_job_aggregate_model_pass(self):
        project_db = InMemoryDBInterface()

        job = self._build_simple_job("1")
        job_2 = self._build_simple_job("2")
        job_2.cancel()
        job_3 = self._build_simple_job("3")

        project = self._build_simple_project()
        experiment, _ = self._build_simple_experiment("1")

        experiment.add_or_update_job(job)
        experiment.add_or_update_job(job_2)
        experiment.add_or_update_job(job_3)

        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        aggregate_model = Model(None, f"{project.id}/{experiment.id}/{job.id}/aggregate_model", 435345)
        handle_job_aggregate_model(aggregate_model, project_db)

        project_from_db = DBObject.load_from_db(
            Project, project.id, project_db)
        self.assertEqual(1, len(project_from_db.get_active_jobs()))
        self.assertEqual(
            job_3.id,
            project_from_db.get_active_jobs()[0]["job_id"])
        
        experiment_from_db = project_from_db.get_experiment(experiment.id)
        job_from_db = experiment_from_db.get_job(job.id)
        job_3_from_db = experiment_from_db.get_job(job_3.id)

        self.assertEqual(
            job_from_db.aggregate_model,
            job_3_from_db.start_model)

    def test_handle_experiment_start_model_pass(self):
        project_db = InMemoryDBInterface()

        experiment, _ = self._build_simple_experiment("1")

        project = self._build_simple_project()
        project.add_or_update_experiment(experiment)
        project.save_to_db(project_db)

        model = Model(None, f"{project.id}/{experiment.id}/start_model", 1232131)
        should_aggregate = handle_experiment_start_model(model, project_db)

        self.assertFalse(should_aggregate)

        loaded_project = DBObject.load_from_db(Project, project.id, project_db)
        loaded_experiment = loaded_project.get_experiment(experiment.id)

        self.assertTrue(loaded_experiment.configuration.is_parameters_set())
