from dependencies.python.fmlaas.controller.cancel_job import \
    CancelJobController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsUser)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import (DBObject, Job, JobConfiguration,
                                              JobFactory, Model, Project,
                                              ProjectPrivilegeTypesEnum,
                                              Status)
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class CancelJobControllerTestCase(AbstractTestCase):

    def test_pass(self):
        job_db = InMemoryDBInterface()
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()
        experiment = self._build_simple_experiment()
        job = self._build_simple_job()

        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        project.save_to_db(project_db)
        job.save_to_db(job_db)

        CancelJobController(
            project_db,
            job_db,
            job.id,
            auth_context).execute()

        db_project = DBObject.load_from_db(
            Project, project.id, project_db)
        db_job = DBObject.load_from_db(Job, job.id, job_db)

        self.assertTrue(db_job.is_cancelled())
        self.assertTrue(job.id not in db_project.get_active_jobs())
        self.assertEqual(0, len(db_project.get_active_jobs()))

    def test_pass_2(self):
        job_db = InMemoryDBInterface()
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()
        experiment = self._build_simple_experiment()

        experiment.start_model = Model("12312414", "12312414/start_model", "123211")
        experiment.current_model = Model("12312414", "12312414/start_model", "123211")

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        job_configuration = JobConfiguration(1, 0, "RANDOM", [])
        start_model = Model("12312414",
                            "12312414/start_model",
                            "123211")
        aggregate_model = Model("1234",
                                "1234/aggregate_model",
                                "123211")

        job = JobFactory.create_job("job_test_id",
                                     job_configuration,
                                     "test_id",
                                     "test_id_2",
                                     ["34553"])
        job.start_model = start_model
        job.aggregate_model = aggregate_model

        job_2 = JobFactory.create_job("job_test_id_2",
                                     job_configuration,
                                     "test_id",
                                     "test_id_2",
                                     ["34553"])

        job_3 = JobFactory.create_job("job_test_id",
                                     job_configuration,
                                     "test_id",
                                     "test_id_2",
                                     ["34553"])
        job_3.cancel()

        experiment.add_job(job)
        experiment.add_job(job_3)
        experiment.add_job(job_2)

        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)
        job.save_to_db(job_db)
        job_2.save_to_db(job_db)
        job_3.save_to_db(job_db)

        CancelJobController(
            project_db,
            job_db,
            job.id,
            auth_context).execute()

        db_project = DBObject.load_from_db(
            Project, project.id, project_db)
        db_job = DBObject.load_from_db(Job, job.id, job_db)
        db_job_2 = DBObject.load_from_db(Job, job_2.id, job_db)

        self.assertTrue(db_job.is_cancelled())
        self.assertTrue(job.id not in db_project.get_active_jobs())
        self.assertEqual(1, len(db_project.get_active_jobs()))
        self.assertTrue(job_2.id in db_project.get_active_jobs())
        self.assertEqual(db_job_2.status, Status.IN_PROGRESS)
        self.assertEqual(
            db_job_2.start_model.to_json(),
            db_job.start_model.to_json())

    def test_pass_3(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.aggregate_model = Model("1234", "1234/1234", "123211")
        job.complete()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        experiment = self._build_simple_experiment()
        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertRaises(
            Exception,
            CancelJobController(project_db_,
                                job_db_,
                                job.id,
                                auth_context).execute)

    def test_get_auth_conditions_pass(self):
        job_db = InMemoryDBInterface()
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()
        job = self._build_simple_job()

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        project.save_to_db(project_db)
        job.save_to_db(job_db)

        controller = CancelJobController(project_db,
                                         job_db,
                                         job.id,
                                         auth_context)

        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)