import unittest

from dependencies.python.fmlaas.device_selection import RandomDeviceSelector
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobSequenceBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.start_job import get_device_selector
from dependencies.python.fmlaas.controller.start_job import create_job
from dependencies.python.fmlaas.controller.start_job import start_job_controller
from dependencies.python.fmlaas.request_processor import AuthContextProcessor


class StartJobControllerTestCase(unittest.TestCase):

    def test_get_device_selector_pass(self):
        device_selector = get_device_selector(
            JobConfiguration(5, 0, "RANDOM", []))

        self.assertEqual(device_selector.__class__, RandomDeviceSelector)

    def test_create_job_pass(self):
        devices = ["123", "234", "345", "3456"]
        job_config = JobConfiguration(4, 0, "RANDOM", [])

        new_job = create_job(devices, "test_id123", "job_sequence_id_123", job_config)

        self.assertIsNotNone(new_job.get_id())
        self.assertEqual(new_job.get_devices(), devices)
        self.assertEqual(new_job.get_project_id(), "test_id123")
        self.assertEqual(new_job.get_job_sequence_id(), "job_sequence_id_123")
        self.assertEqual(
            job_config.to_json(),
            new_job.get_configuration().to_json())

    def test_start_job_controller_pass_1(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
        job_builder.set_job_sequence_id("job_sequence_id_123")
        job_builder.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(
            Model(
                "12312414",
                "12312414/start_model",
                "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_id_123"
        job_sequence = builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        job.save_to_db(job_db)
        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        new_job_id = start_job_controller(
            job_db, project_db, project.get_id(), job_sequence.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context_processor)
        new_job = DBObject.load_from_db(Job, new_job_id, job_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)

        self.assertEqual(updated_project.get_active_jobs(), [job.get_id()])
        self.assertTrue(updated_project.contains_job(new_job_id))

    def test_start_job_controller_pass_2(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_id_123"
        job_sequence = builder.build()
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        new_job_id = start_job_controller(
            job_db, project_db, project.get_id(), job_sequence.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context_processor)
        new_job = DBObject.load_from_db(Job, new_job_id, job_db)
        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)

        self.assertEqual(new_job.get_devices(), ["34553"])

        self.assertEqual(updated_project.get_active_jobs(), [new_job_id])
        self.assertTrue(updated_project.contains_job(new_job_id))

    def test_start_job_controller_pass_3(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
        job_builder.set_job_sequence_id("job_sequence_id_123")
        job_builder.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(
            Model(
                "12312414",
                "12312414/start_model",
                "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()
        job.cancel()

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_id_123"
        job_sequence = builder.build()
        job_sequence.add_job(job)
        job_sequence.proceed_to_next_job()
        project.add_or_update_job_sequence(job_sequence)

        job.save_to_db(job_db)
        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        new_job_id = start_job_controller(
            job_db, project_db, project.get_id(), job_sequence.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context_processor)
        new_job = DBObject.load_from_db(Job, new_job_id, job_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)

        self.assertEqual(
            job.get_end_model().to_json(),
            new_job.get_start_model().to_json())
        self.assertEqual(updated_project.get_active_jobs(), [new_job_id])
        self.assertTrue(updated_project.contains_job(new_job_id))

    def test_start_job_controller_pass_4(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
        job_builder.set_job_sequence_id("job_sequence_id_123")
        job_builder.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(
            Model(
                "12312414",
                "12312414/start_model",
                "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_id_123"
        job_sequence = builder.build()
        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        job.save_to_db(job_db)
        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        new_job_id = start_job_controller(
            job_db, project_db, project.get_id(), job_sequence.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context_processor)
        new_job_id_2 = start_job_controller(
            job_db, project_db, project.get_id(), job_sequence.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context_processor)
        new_job_id_3 = start_job_controller(
            job_db, project_db, project.get_id(), job_sequence.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context_processor)
        new_job_id_4 = start_job_controller(
            job_db, project_db, project.get_id(), job_sequence.id, JobConfiguration(
                1, 0, "RANDOM", []), auth_context_processor)
        new_job = DBObject.load_from_db(Job, new_job_id, job_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)

        self.assertEqual(
            job.get_end_model().to_json(),
            new_job.get_start_model().to_json())
        self.assertEqual(updated_project.get_active_jobs(), [new_job_id])
        self.assertTrue(updated_project.contains_job(new_job_id))

    def test_start_job_controller_fail_no_devices(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_id_123"
        job_sequence = builder.build()
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(
            ValueError,
            start_job_controller,
            job_db,
            project_db,
            project.get_id(),
            job_sequence.id,
            JobConfiguration(
                1,
                0,
                "RANDOM",
                []),
            auth_context_processor)

    def test_start_job_controller_fail(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)
        project.add_or_update_member(
            "user_123456", ProjectPrivilegeTypesEnum.READ_ONLY)

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_id_123"
        job_sequence = builder.build()
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_123456"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(
            RequestForbiddenException,
            start_job_controller,
            job_db,
            project_db,
            project.get_id(),
            job_sequence.id,
            JobConfiguration(
                1,
                0,
                "RANDOM",
                []),
            auth_context_processor)

    def test_start_job_controller_fail_2(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)
        project.add_or_update_member(
            "user_123456", ProjectPrivilegeTypesEnum.READ_ONLY)

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_id_123"
        job_sequence = builder.build()
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_1234567"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(
            RequestForbiddenException,
            start_job_controller,
            job_db,
            project_db,
            project.get_id(),
            job_sequence.id,
            JobConfiguration(
                1,
                0,
                "RANDOM",
                []),
            auth_context_processor)

    def test_start_job_controller_fail_3(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)
        project.add_or_update_member(
            "user_123456", ProjectPrivilegeTypesEnum.READ_ONLY)

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_id_123"
        job_sequence = builder.build()
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "34553"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(
            RequestForbiddenException,
            start_job_controller,
            job_db,
            project_db,
            project.get_id(),
            job_sequence.id,
            JobConfiguration(
                1,
                0,
                "RANDOM",
                []),
            auth_context_processor)
