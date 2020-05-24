import unittest

from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import JobStatus
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.submit_job_start_model import submit_job_start_model_controller
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

class SubmitJobStartModelControllerTestCase(unittest.TestCase):

    def _build_default_project(self):
        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        project = builder.build()

        project.add_device("12312313123")
        project.add_or_update_member("user_12345", ProjectPrivilegeTypesEnum.ADMIN)
        project.add_or_update_member("user_123456", ProjectPrivilegeTypesEnum.READ_ONLY)

        return project

    def _build_default_job(self, id):
        job_builder = JobBuilder()
        job_builder.set_id(id)
        job_builder.set_parent_project_id("test_id")
        job_builder.set_configuration(JobConfiguration(1, 0, "RANDOM", []).to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()

        return job

    def test_pass(self):
        job_db = InMemoryDBInterface()
        project_db = InMemoryDBInterface()

        project = self._build_default_project()
        job = self._build_default_job("job_test_id")

        project.save_to_db(project_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        can_submit_start_model, presigned_url = submit_job_start_model_controller(project_db, job_db, job.get_id(), auth_context_processor)

        self.assertTrue(can_submit_start_model)
        self.assertIsNotNone(presigned_url)

    def test_fail_not_authorized_user(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        project = self._build_default_project()
        job = self._build_default_job("job_test_id")

        project.save_to_db(project_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, submit_job_start_model_controller, project_db, job_db, "job_test_id", auth_context_processor)

    def test_fail_not_authorized_device(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        project = self._build_default_project()
        job = self._build_default_job("job_test_id")

        project.save_to_db(project_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "34553"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, submit_job_start_model_controller, project_db, job_db, "job_test_id", auth_context_processor)

    def test_fail_not_authorized_job(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, submit_job_start_model_controller, job_db, project_db, "woot", auth_context_processor)
