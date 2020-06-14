from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import Experiment
from .abstract_model_testcase import AbstractModelTestCase


class ExperimentTestCase(AbstractModelTestCase):

    def test_to_json_pass(self):
        experiment, json_data = self._build_default_experiment()

        self.assertEqual(json_data, experiment.to_json())

    def test_from_json_pass(self):
        orig_experiment, json_data = self._build_default_experiment()

        experiment = Experiment.from_json(json_data)

        self.assertEqual(orig_experiment, experiment)

    def test_set_get_start_model_pass_1(self):
        experiment, _ = self._build_default_experiment()

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        experiment.start_model = start_model

        self.assertEqual(experiment.start_model, start_model)

    def test_get_current_job_pass_1(self):
        experiment, _ = self._build_default_experiment()

        job_1 = self._build_job(1)

        experiment.add_job(job_1)

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        experiment.start_model = start_model

        self.assertEqual("test_id_1", experiment.current_job)

    def test_get_current_job_pass_2(self):
        experiment, _ = self._build_default_experiment()

        job_1 = self._build_job(1)
        job_2 = self._build_job(2)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)

        experiment.add_job(job_1)
        experiment.add_job(job_2)
        experiment.add_job(job_3)
        experiment.add_job(job_4)

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        experiment.start_model = start_model

        self.assertEqual("test_id_1", experiment.current_job)

    def test_add_get_jobs_pass(self):
        experiment, _ = self._build_default_experiment()

        self.assertEqual([], experiment.jobs)

        job_1 = self._build_job(1)
        job_2 = self._build_job(2)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)

        experiment.add_job(job_1)
        experiment.add_job(job_2)
        experiment.add_job(job_3)
        experiment.add_job(job_4)

        self.assertEqual([
            "test_id_1",
            "test_id_2",
            "test_id_3",
            "test_id_4"],
            experiment.jobs)

    def test_proceed_to_next_job_pass(self):
        experiment, _ = self._build_default_experiment()

        job_1 = self._build_job(1)
        job_2 = self._build_job(2)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)

        experiment.add_job(job_1)
        experiment.add_job(job_2)
        experiment.add_job(job_3)
        experiment.add_job(job_4)

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        experiment.start_model = start_model

        self.assertEqual("test_id_1", experiment.current_job)

        experiment.proceed_to_next_job()

        self.assertEqual("test_id_2", experiment.current_job)

        experiment.proceed_to_next_job()

        self.assertEqual("test_id_3", experiment.current_job)

        experiment.proceed_to_next_job()

        self.assertEqual("test_id_4", experiment.current_job)

        experiment.proceed_to_next_job()

        self.assertEqual("test_id_4", experiment.current_job)

    def test_set_get_hyperparameters_pass(self):
        experiment, _ = self._build_default_experiment()

        hyperparameters = {
            "lr" : "0.005"
        }
        experiment.hyperparameters = hyperparameters

        self.assertEqual(hyperparameters, experiment.hyperparameters)

    def test_equals_pass(self):
        experiment, _ = self._build_default_experiment()
        experiment_2, _ = self._build_default_experiment()
        experiment_3, _ = self._build_default_experiment()

        experiment_3.add_job(self._build_job(1))

        self.assertEqual(experiment, experiment_2)
        self.assertNotEqual(experiment, experiment_3)
        self.assertNotEqual(experiment_2, experiment_3)

    def test_is_active_pass(self):
        experiment, _ = self._build_default_experiment()

        job_1 = self._build_job(1)
        job_2 = self._build_job(2)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)

        self.assertFalse(experiment.is_active)

        experiment.add_job(job_1)
        experiment.add_job(job_2)
        experiment.add_job(job_3)
        experiment.add_job(job_4)

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        experiment.start_model = start_model

        self.assertTrue(experiment.is_active)

        experiment.proceed_to_next_job()

        self.assertTrue(experiment.is_active)

        experiment.proceed_to_next_job()

        self.assertTrue(experiment.is_active)

        experiment.proceed_to_next_job()

        self.assertTrue(experiment.is_active)

        experiment.proceed_to_next_job()

        self.assertFalse(experiment.is_active)

    def test_is_active_pass_2(self):
        experiment, _ = self._build_default_experiment()

        job_1 = self._build_job(1)
        job_2 = self._build_job(2)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)
        job_5 = self._build_job(5)

        self.assertFalse(experiment.is_active)

        experiment.add_job(job_1)
        experiment.add_job(job_2)
        experiment.add_job(job_3)
        experiment.add_job(job_4)

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        experiment.start_model = start_model

        experiment.proceed_to_next_job()
        experiment.proceed_to_next_job()
        experiment.proceed_to_next_job()
        experiment.proceed_to_next_job()

        self.assertFalse(experiment.is_active)

        experiment.add_job(job_5)

        self.assertTrue(experiment.is_active)

    def test_is_start_model_set_pass(self):
        experiment, _ = self._build_default_experiment()

        self.assertFalse(experiment.is_start_model_set())

    def test_is_start_model_set_pass_2(self):
        experiment, _ = self._build_default_experiment()
        experiment.start_model = Model("123123", "123123/start_model", "1231213")

        self.assertTrue(experiment.is_start_model_set())
