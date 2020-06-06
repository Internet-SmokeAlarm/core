from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobSequence
from .abstract_model_testcase import AbstractModelTestCase


class JobSequenceTestCase(AbstractModelTestCase):

    def test_to_json_pass(self):
        sequence, json_data = self._build_default_job_sequence()

        self.assertEqual(json_data, sequence.to_json())

    def test_from_json_pass(self):
        orig_sequence, json_data = self._build_default_job_sequence()

        sequence = JobSequence.from_json(json_data)

        self.assertEqual(orig_sequence, sequence)

    def test_set_get_start_model_pass_1(self):
        sequence, _ = self._build_default_job_sequence()

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        sequence.start_model = start_model

        self.assertEqual(sequence.start_model, start_model)

    def test_get_current_job_pass_1(self):
        sequence, _ = self._build_default_job_sequence()

        job_1 = self._build_job(1)

        sequence.add_job(job_1)

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        sequence.start_model = start_model

        self.assertEqual("test_id_1", sequence.current_job)

    def test_get_current_job_pass_2(self):
        sequence, _ = self._build_default_job_sequence()

        job_1 = self._build_job(1)
        job_2 = self._build_job(2)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)

        sequence.add_job(job_1)
        sequence.add_job(job_2)
        sequence.add_job(job_3)
        sequence.add_job(job_4)

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        sequence.start_model = start_model

        self.assertEqual("test_id_1", sequence.current_job)

    def test_add_get_jobs_pass(self):
        sequence, _ = self._build_default_job_sequence()

        self.assertEqual([], sequence.jobs)

        job_1 = self._build_job(1)
        job_2 = self._build_job(2)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)

        sequence.add_job(job_1)
        sequence.add_job(job_2)
        sequence.add_job(job_3)
        sequence.add_job(job_4)

        self.assertEqual([
            "test_id_1",
            "test_id_2",
            "test_id_3",
            "test_id_4"],
            sequence.jobs)

    def test_proceed_to_next_job_pass(self):
        sequence, _ = self._build_default_job_sequence()

        job_1 = self._build_job(1)
        job_2 = self._build_job(2)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)

        sequence.add_job(job_1)
        sequence.add_job(job_2)
        sequence.add_job(job_3)
        sequence.add_job(job_4)

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        sequence.start_model = start_model

        self.assertEqual("test_id_1", sequence.current_job)

        sequence.proceed_to_next_job()

        self.assertEqual("test_id_2", sequence.current_job)

        sequence.proceed_to_next_job()

        self.assertEqual("test_id_3", sequence.current_job)

        sequence.proceed_to_next_job()

        self.assertEqual("test_id_4", sequence.current_job)

        sequence.proceed_to_next_job()

        self.assertEqual("test_id_4", sequence.current_job)

    def test_set_get_hyperparameters_pass(self):
        sequence, _ = self._build_default_job_sequence()

        hyperparameters = {
            "lr" : "0.005"
        }
        sequence.hyperparameters = hyperparameters

        self.assertEqual(hyperparameters, sequence.hyperparameters)

    def test_equals_pass(self):
        sequence, _ = self._build_default_job_sequence()
        sequence_2, _ = self._build_default_job_sequence()
        sequence_3, _ = self._build_default_job_sequence()

        sequence_3.add_job(self._build_job(1))

        self.assertEqual(sequence, sequence_2)
        self.assertNotEqual(sequence, sequence_3)
        self.assertNotEqual(sequence_2, sequence_3)

    def test_is_active_pass(self):
        sequence, _ = self._build_default_job_sequence()

        job_1 = self._build_job(1)
        job_2 = self._build_job(2)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)

        self.assertFalse(sequence.is_active)

        sequence.add_job(job_1)
        sequence.add_job(job_2)
        sequence.add_job(job_3)
        sequence.add_job(job_4)

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        sequence.start_model = start_model

        self.assertTrue(sequence.is_active)

        sequence.proceed_to_next_job()

        self.assertTrue(sequence.is_active)

        sequence.proceed_to_next_job()

        self.assertTrue(sequence.is_active)

        sequence.proceed_to_next_job()

        self.assertTrue(sequence.is_active)

        sequence.proceed_to_next_job()

        self.assertFalse(sequence.is_active)

    def test_is_active_pass_2(self):
        sequence, _ = self._build_default_job_sequence()

        job_1 = self._build_job(1)
        job_2 = self._build_job(2)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)
        job_5 = self._build_job(5)

        self.assertFalse(sequence.is_active)

        sequence.add_job(job_1)
        sequence.add_job(job_2)
        sequence.add_job(job_3)
        sequence.add_job(job_4)

        start_model = Model(
            "123dafasdf34sdfsdf",
            "adfsfsdfs/123dafasdf34sdfsdf/start_model",
            "12312311")
        sequence.start_model = start_model

        sequence.proceed_to_next_job()
        sequence.proceed_to_next_job()
        sequence.proceed_to_next_job()
        sequence.proceed_to_next_job()

        self.assertFalse(sequence.is_active)

        sequence.add_job(job_5)

        self.assertTrue(sequence.is_active)

    def test_is_start_model_set_pass(self):
        sequence, _ = self._build_default_job_sequence()

        self.assertFalse(sequence.is_start_model_set())

    def test_is_start_model_set_pass_2(self):
        sequence, _ = self._build_default_job_sequence()
        sequence.start_model = Model("123123", "123123/start_model", "1231213")

        self.assertTrue(sequence.is_start_model_set())
