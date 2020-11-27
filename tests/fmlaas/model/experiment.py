from dependencies.python.fmlaas.utils.time.epoch_time import get_epoch_time
from dependencies.python.fmlaas.model import (DeviceSelectionStrategy,
                                              Experiment, JobConfiguration,
                                              Model)
from dependencies.python.fmlaas.model.termination_criteria import \
    DurationTerminationCriteria

from .abstract_model_testcase import AbstractModelTestCase


class ExperimentTestCase(AbstractModelTestCase):

    def test_to_json_pass(self):
        experiment, json_repr = self._create_experiment("1")
        
        self.assertEqual(json_repr, experiment.to_json())

    def test_from_json_pass(self):
        orig_experiment, json_repr = self._create_experiment("1")

        experiment = Experiment.from_json(json_repr)

        self.assertEqual(orig_experiment, experiment)
    
    def test_contains_job_pass(self):
        exp, _ = self._create_experiment("1")

        job_1, _ = self._create_job("1")

        self.assertFalse(exp.contains_job(job_1.id))

        job_2, _ = self._create_job("2")
        exp.add_or_update_job(job_2)

        self.assertTrue(exp.contains_job(job_2.id))
        self.assertFalse(exp.contains_job(job_1.id))

        job_3, _ = self._create_job("3")
        exp.add_or_update_job(job_3)

        self.assertTrue(exp.contains_job(job_3.id))
        self.assertTrue(exp.contains_job(job_2.id))
        self.assertFalse(exp.contains_job(job_1.id))

    def test_add_or_update_job_pass_1(self):
        """
        1. Test adding a job to a new experiment
        """
        exp, _ = self._create_experiment("1")
        job_1, _ = self._create_job("1")

        exp.add_or_update_job(job_1)

        self.assertEqual(exp.current_job, job_1)
        self.assertEqual(exp._current_job_id, job_1.id)
        self.assertEqual(exp.current_job.start_model, exp.configuration.parameters)
    
    def test_add_or_update_job_pass_2(self):
        """
        1. Add a job to a new experiment
        2. Complete the job, and re-add the job to the experiment
        3. Create a new job, add it to the experiment
        """
        job_1_id = "1"
        experiment_id = "1"
        project_id = "test123"
        aggregate_model = Model("123", f"{project_id}/{experiment_id}/{job_1_id}/aggregate_model", 12345)

        exp, _ = self._create_experiment(experiment_id, project_id=project_id)
        job_1, _ = self._create_job(job_1_id)
        job_2, _ = self._create_job("2")

        exp.add_or_update_job(job_1)

        job_1.complete()
        job_1.aggregate_model = aggregate_model
        exp.add_or_update_job(job_1)

        exp.add_or_update_job(job_2)

        self.assertEqual(exp.current_job, job_2)
        self.assertEqual(exp._current_job_id, job_2.id)
        self.assertEqual(exp.current_job.start_model, aggregate_model)
    
    def test_add_or_update_job_pass_3(self):
        """
        1. Add a job to a new experiment
        2. Create a new job, add it to the experiment
        3. Complete the first job, and re-add the job to the experiment
        """
        job_1_id = "1"
        experiment_id = "1"
        project_id = "test123"
        aggregate_model = Model("123", f"{project_id}/{experiment_id}/{job_1_id}/aggregate_model", 12345)

        exp, _ = self._create_experiment(experiment_id, project_id=project_id)
        job_1, _ = self._create_job(job_1_id)
        job_2, _ = self._create_job("2")

        exp.add_or_update_job(job_1)
        exp.add_or_update_job(job_2)

        job_1.complete()
        job_1.aggregate_model = aggregate_model
        exp.add_or_update_job(job_1)

        self.assertEqual(exp.current_job, job_2)
        self.assertEqual(exp.current_job.start_model, aggregate_model)
    
    def test_add_or_update_job_pass_4(self):
        """
        1. Add a job to a new experiment
        2. Cancel the job, and re-add the job to the experiment
        3. Create a new job, add it to the experiment
        """
        exp, _ = self._create_experiment("1")
        job_1, _ = self._create_job("1")
        job_2, _ = self._create_job("2")

        exp.add_or_update_job(job_1)

        job_1.cancel()
        exp.add_or_update_job(job_1)

        exp.add_or_update_job(job_2)

        self.assertEqual(exp.current_job, job_2)
        self.assertEqual(exp._current_job_id, job_2.id)
        self.assertEqual(exp.current_job.start_model, job_1.start_model)
    
    def test_handle_termination_check_pass(self):
        """
        1. Add 2 jobs to a new experiment (first of which times out)
        2. Handle termination check, verify the experiment updates to job 2
        """
        custom_config = JobConfiguration(2, 0, DeviceSelectionStrategy.RANDOM, [
            DurationTerminationCriteria(0, get_epoch_time())
        ])

        exp, _ = self._create_experiment("1")
        job_1, _ = self._create_job("1")
        job_2, _ = self._create_job("2")

        job_1.configuration = custom_config

        exp.add_or_update_job(job_1)
        exp.add_or_update_job(job_2)

        exp.handle_termination_check()

        self.assertEqual(exp.current_job, job_2)

    def test_equals_pass(self):
        experiment, _ = self._create_experiment("1")
        experiment_2, _ = self._create_experiment("1")
        experiment_3, _ = self._create_experiment("1")

        job_1, _ = self._create_job("1")

        experiment_3.add_or_update_job(job_1)

        self.assertEqual(experiment, experiment_2)
        self.assertNotEqual(experiment, experiment_3)
        self.assertNotEqual(experiment_2, experiment_3)

    def test_get_job_pass(self):
        experiment, _ = self._create_experiment("1")
        job_1, _ = self._create_job("1")

        experiment.add_or_update_job(job_1)

        self.assertEqual(job_1, experiment.get_job(job_1.id))
    
    def test_get_next_job_id_pass(self):
        experiment, _ = self._create_experiment("1")
        job_1, _ = self._create_job("1")
        job_2, _ = self._create_job("2")
        job_3, _ = self._create_job("3")

        experiment.add_or_update_job(job_1)
        experiment.add_or_update_job(job_2)
        experiment.add_or_update_job(job_3)

        self.assertEqual("4", experiment.get_next_job_id())