import unittest

from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.model import JobStatus
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.cancel_job import cancel_job_controller


class CancelJobControllerTestCase(unittest.TestCase):

    def _build_default_project(self):
        project_builder = ProjectBuilder()
        project_builder.set_id("test_id")
        project_builder.set_name("test_name")

        project = project_builder.build()
        project.add_device("12344")
        project.create_job_path("1234432414")
        project.add_current_job_id("1234432414")
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.READ_ONLY)

        return project

    def _build_default_job(self):
        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_parent_project_id("test_id")
        job_builder.set_parent_job_sequence_id("test_id_2")
        job_builder.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(
            Model(
                "12312414",
                "12312414/start_model",
                "123211").to_json())
        job_builder.set_aggregate_model(
            Model(
                "1234",
                "1234/aggregate_model",
                "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()

        return job

    def test_pass(self):
        job_db = InMemoryDBInterface()
        project_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        project = builder.build()
        project.add_device("12312313123")
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_parent_project_id("test_id")
        job_builder.set_parent_job_sequence_id("test_id_2")
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

        project.create_job_path(job.get_id())
        project.add_current_job_id(job.get_id())

        project.save_to_db(project_db)
        job.save_to_db(job_db)

        cancel_job_controller(
            project_db,
            job_db,
            job.get_id(),
            auth_context_processor)

        db_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)
        db_job = DBObject.load_from_db(Job, job.get_id(), job_db)

        self.assertTrue(db_job.is_cancelled())
        self.assertTrue(job.get_id() not in db_project.get_current_job_ids())
        self.assertEqual(0, len(db_project.get_current_job_ids()))

    def test_pass_2(self):
        job_db = InMemoryDBInterface()
        project_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        project = builder.build()
        project.add_device("12312313123")
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_parent_project_id("test_id")
        job_builder.set_parent_job_sequence_id("test_id_2")
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

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id_2")
        job_builder.set_parent_project_id("test_id")
        job_builder.set_parent_job_sequence_id("test_id_2")
        job_builder.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder.set_devices(["34553"])
        job_2 = job_builder.build()

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id_3")
        job_builder.set_parent_project_id("test_id")
        job_builder.set_parent_job_sequence_id("test_id_2")
        job_builder.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder.set_devices(["34553"])
        job_3 = job_builder.build()
        job_3.cancel()

        project.create_job_path(job.get_id())
        project.add_current_job_id(job.get_id())
        project.add_job_to_path_prev_id(job.get_id(), job_3.get_id())
        project.add_job_to_path_prev_id(job_3.get_id(), job_2.get_id())

        project.save_to_db(project_db)
        job.save_to_db(job_db)
        job_2.save_to_db(job_db)
        job_3.save_to_db(job_db)

        cancel_job_controller(
            project_db,
            job_db,
            job.get_id(),
            auth_context_processor)

        db_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)
        db_job = DBObject.load_from_db(Job, job.get_id(), job_db)
        db_job_2 = DBObject.load_from_db(Job, job_2.get_id(), job_db)

        self.assertTrue(db_job.is_cancelled())
        self.assertTrue(job.get_id() not in db_project.get_current_job_ids())
        self.assertEqual(1, len(db_project.get_current_job_ids()))
        self.assertTrue(job_2.get_id() in db_project.get_current_job_ids())
        self.assertEqual(db_job_2.get_status(), JobStatus.IN_PROGRESS)
        self.assertEqual(
            db_job_2.get_start_model().to_json(),
            db_job.get_start_model().to_json())

    def test_pass_3(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_default_job()
        job.set_aggregate_model(Model("1234", "1234/1234", "123211"))
        job.complete()
        job.save_to_db(job_db_)

        project = self._build_default_project()
        project.create_job_path(job.get_id())
        project.add_current_job_id(job.get_id())
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(
            Exception,
            cancel_job_controller,
            project_db_,
            job_db_,
            job.get_id(),
            auth_context_processor)

    def test_fail_not_authorized_user(self):
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

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_parent_project_id("test_id")
        job_builder.set_parent_job_sequence_id("test_id_2")
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

        project.save_to_db(project_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_123456"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(
            RequestForbiddenException,
            cancel_job_controller,
            project_db,
            job_db,
            "job_test_id",
            auth_context_processor)

    def test_fail_not_authorized_device(self):
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

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_parent_project_id("test_id")
        job_builder.set_parent_job_sequence_id("test_id_2")
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

        project.save_to_db(project_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "34553"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(
            RequestForbiddenException,
            cancel_job_controller,
            project_db,
            job_db,
            "job_test_id",
            auth_context_processor)

    def test_fail_not_authorized(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_123456"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(
            RequestForbiddenException,
            cancel_job_controller,
            job_db,
            project_db,
            "woot",
            auth_context_processor)
