import unittest

from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobSequenceBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.get_job_start_model import get_job_start_model_controller
from dependencies.python.fmlaas.request_processor import AuthContextProcessor


class GetJobStartModelControllerTestCase(unittest.TestCase):

    def _build_default_project(self):
        project_builder = ProjectBuilder()
        project_builder.set_id("test_id")
        project_builder.set_name("test_name")

        project = project_builder.build()
        project.add_device("12344")
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.READ_ONLY)

        return project

    def _build_default_job(self):
        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
        job_builder.set_job_sequence_id("job_sequence_1")
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

    def test_pass_1(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_default_job()
        job.save_to_db(job_db_)

        project = self._build_default_project()

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_1"
        job_sequence = builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        presigned_url = get_job_start_model_controller(project_db_,
                                                       job_db_,
                                                       project.get_id(),
                                                       job.get_id(),
                                                       auth_context)
        self.assertIsNotNone(presigned_url)

    def test_pass_2(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_default_job()
        job.save_to_db(job_db_)

        project = self._build_default_project()

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_1"
        job_sequence = builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "34553"
        }
        auth_context = AuthContextProcessor(auth_json)
        presigned_url = get_job_start_model_controller(project_db_,
                                                       job_db_,
                                                       project.get_id(),
                                                       job.get_id(),
                                                       auth_context)
        self.assertIsNotNone(presigned_url)

    def test_fail_not_authorized_1(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_default_job()
        job.save_to_db(job_db_)

        project = self._build_default_project()

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_1"
        job_sequence = builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "123445"
        }
        auth_context = AuthContextProcessor(auth_json)
        self.assertRaises(
            RequestForbiddenException,
            get_job_start_model_controller,
            project_db_,
            job_db_,
            project.get_id(),
            job.get_id(),
            auth_context)

    def test_fail_not_authorized_2(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_default_job()
        job.save_to_db(job_db_)

        project = self._build_default_project()

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_1"
        job_sequence = builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "123445"
        }
        auth_context = AuthContextProcessor(auth_json)
        self.assertRaises(
            RequestForbiddenException,
            get_job_start_model_controller,
            project_db_,
            job_db_,
            project.get_id(),
            job.get_id(),
            auth_context)

    def test_fail_not_authorized_3(self):
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
            get_job_start_model_controller,
            project_db_,
            job_db_,
            project.get_id(),
            job.get_id(),
            auth_context)

    def test_fail_not_authorized_4(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_default_job()
        job.save_to_db(job_db_)

        project = self._build_default_project()

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_1"
        job_sequence = builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        self.assertRaises(
            RequestForbiddenException,
            get_job_start_model_controller,
            project_db_,
            job_db_,
            project.get_id(),
            job.get_id(),
            auth_context)
