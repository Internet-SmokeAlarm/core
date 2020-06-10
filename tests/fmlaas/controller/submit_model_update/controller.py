import unittest

from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.submit_model_update import submit_model_update_controller
from dependencies.python.fmlaas.request_processor import AuthContextProcessor


class SubmitModelUpdateControllerTestCase(unittest.TestCase):

    def _build_default_project(self):
        project_builder = ProjectBuilder()
        project_builder.set_id("test_id")
        project_builder.set_name("test_name")

        project = project_builder.build()
        project.add_device("12344")
        project.create_job_path("1234432414")
        project.add_current_job_id("1234432414")
        project.add_or_update_member(
            "user_123456", ProjectPrivilegeTypesEnum.OWNER)

        return project

    def _build_default_job(self):
        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
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
        job_builder.set_devices(["12344"])
        job = job_builder.build()

        return job

    def test_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_default_job()
        job.save_to_db(job_db_)

        project = self._build_default_project()
        project.create_job_path(job.get_id())
        project.add_current_job_id(job.get_id())
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        can_submit_model_to_job, presigned_url = submit_model_update_controller(project_db_,
                                                                                job_db_,
                                                                                project.get_id(),
                                                                                job.get_id(),
                                                                                auth_context)
        self.assertTrue(can_submit_model_to_job)
        self.assertIsNotNone(presigned_url)
        self.assertTrue("device_models" in presigned_url["fields"]["key"])

    def test_fail_not_authorized_user(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_default_job()
        job.save_to_db(job_db_)

        project = self._build_default_project()
        project.create_job_path(job.get_id())
        project.add_current_job_id(job.get_id())
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_123456"
        }
        auth_context = AuthContextProcessor(auth_json)
        self.assertRaises(
            RequestForbiddenException,
            submit_model_update_controller,
            project_db_,
            job_db_,
            project.get_id(),
            job.get_id(),
            auth_context)

    def test_fail_not_authorized_device(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_default_job()
        job.save_to_db(job_db_)

        project = self._build_default_project()
        project.create_job_path(job.get_id())
        project.add_current_job_id(job.get_id())
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "123445"
        }
        auth_context = AuthContextProcessor(auth_json)
        self.assertRaises(
            RequestForbiddenException,
            submit_model_update_controller,
            project_db_,
            job_db_,
            project.get_id(),
            job.get_id(),
            auth_context)

    def test_fail_not_authorized_job(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_default_job()
        job.save_to_db(job_db_)

        project = self._build_default_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        self.assertRaises(
            RequestForbiddenException,
            submit_model_update_controller,
            project_db_,
            job_db_,
            project.get_id(),
            job.get_id(),
            auth_context)
