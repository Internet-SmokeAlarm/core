from dependencies.python.fmlaas.device_selection import RandomDeviceSelector
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import ExperimentBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.start_job import StartJobController
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from ..abstract_testcase import AbstractTestCase

class StartJobControllerTestCase(AbstractTestCase):

    def test_get_device_selector_pass(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db)

        project = self._build_simple_project()

        builder = ExperimentBuilder()
        builder.id = "test_experiment_1"
        experiment = builder.build()

        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = StartJobController(
            job_db, project_db, project.get_id(), experiment.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context)
        device_selector = controller.get_device_selector()

        self.assertEqual(device_selector.__class__, RandomDeviceSelector)

    def test_create_job_pass(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db)

        project = self._build_simple_project()
        project.add_device("123")
        project.add_device("234")
        project.add_device("345")

        builder = ExperimentBuilder()
        builder.id = "test_experiment_1"
        experiment = builder.build()

        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        job_config = JobConfiguration(4, 0, "RANDOM", [])
        controller = StartJobController(
            job_db, project_db, project.get_id(), experiment.id, job_config, auth_context)
        device_selector = controller.get_device_selector()
        new_job = controller.create_job(["12344", "123", "234", "345"])

        self.assertIsNotNone(new_job.get_id())
        self.assertEqual(new_job.get_devices(), ["12344", "123", "234", "345"])
        self.assertEqual(new_job.get_project_id(), "test_id")
        self.assertEqual(new_job.get_experiment_id(), "test_experiment_1")
        self.assertEqual(job_config, new_job.get_configuration())

    def test_pass_1(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db)

        project = self._build_simple_project()

        builder = ExperimentBuilder()
        builder.id = "test_experiment_1"
        experiment = builder.build()

        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        new_job = StartJobController(
            job_db, project_db, project.get_id(), experiment.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context).execute()
        new_job = DBObject.load_from_db(Job, new_job.get_id(), job_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)

        self.assertEqual(updated_project.get_active_jobs(), [job.get_id()])
        self.assertTrue(updated_project.contains_job(new_job.get_id()))

    def test_pass_2(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()


        project = self._build_simple_project()

        builder = ExperimentBuilder()
        builder.id = "test_experiment_1"
        experiment = builder.build()
        experiment.current_model = Model(
            "1234",
            "1234/start_model",
            "123211")
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        new_job = StartJobController(
            job_db, project_db, project.get_id(), experiment.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context).execute()
        new_job = DBObject.load_from_db(Job, new_job.get_id(), job_db)
        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)

        self.assertEqual(new_job.get_devices(), ["12344"])

        self.assertEqual(updated_project.get_active_jobs(), [new_job.get_id()])
        self.assertTrue(updated_project.contains_job(new_job.get_id()))

    def test_pass_3(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.cancel()
        job.save_to_db(job_db)

        project = self._build_simple_project()

        builder = ExperimentBuilder()
        builder.id = "test_experiment_1"
        experiment = builder.build()
        experiment.current_model = Model(
            "1234",
            "1234/aggregate_model",
            "123211")

        experiment.add_job(job)
        experiment.proceed_to_next_job()
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        new_job = StartJobController(
            job_db, project_db, project.get_id(), experiment.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context).execute()
        new_job = DBObject.load_from_db(Job, new_job.get_id(), job_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)

        self.assertEqual(
            job.get_end_model().to_json(),
            new_job.get_start_model().to_json())
        self.assertEqual(updated_project.get_active_jobs(), [new_job.get_id()])
        self.assertTrue(updated_project.contains_job(new_job.get_id()))

    def test_pass_4(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.cancel()
        job.save_to_db(job_db)

        project = self._build_simple_project()

        builder = ExperimentBuilder()
        builder.id = "test_experiment_1"
        experiment = builder.build()
        experiment.current_model = Model(
            "1234",
            "1234/aggregate_model",
            "123211")

        experiment.add_job(job)
        experiment.proceed_to_next_job()
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        new_job = StartJobController(
            job_db, project_db, project.get_id(), experiment.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context).execute()
        new_job_2 = StartJobController(
            job_db, project_db, project.get_id(), experiment.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context).execute()
        new_job_3 = StartJobController(
            job_db, project_db, project.get_id(), experiment.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context).execute()
        new_job_4 = StartJobController(
            job_db, project_db, project.get_id(), experiment.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context).execute()
        new_job = DBObject.load_from_db(Job, new_job.get_id(), job_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)

        self.assertEqual(job.get_end_model(), new_job.get_start_model())
        self.assertEqual(updated_project.get_active_jobs(), [new_job.get_id()])
        self.assertTrue(updated_project.contains_job(new_job.get_id()))

    def test_fail_no_devices(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db)

        project = self._build_simple_project()

        builder = ExperimentBuilder()
        builder.id = "test_experiment_1"
        experiment = builder.build()

        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertRaises(
            ValueError,
            StartJobController(job_db,
                               project_db,
                               project.get_id(),
                               experiment.id,
                               JobConfiguration(
                                   5,
                                   0,
                                   "RANDOM",
                                   []),
                               auth_context).execute)
