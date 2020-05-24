import unittest

from dependencies.python.fmlaas.controller.delete_project import delete_project_controller
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

class DeleteProjectControllerTestCase(unittest.TestCase):

    def _build_default_project(self):
        project_builder = ProjectBuilder()
        project_builder.set_id("test_id")
        project_builder.set_name("test_name")

        return project_builder.build()

    def _build_default_job(self):
        job_builder = JobBuilder()
        job_builder.set_id("2345")
        job_builder.set_parent_project_id("test_id")
        configuration = JobConfiguration(1, 0, "RANDOM", [])
        job_builder.set_configuration(configuration.to_json())
        job_builder.set_devices(["3456"])
        job_builder.set_start_model(Model("1234", "1234/1234", "123211").to_json())

        return job_builder.build()

    def test_pass_1(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        project = self._build_default_project()
        job = self._build_default_job()
        project.create_job_path("2345")
        project.add_or_update_member("user12344", ProjectPrivilegeTypesEnum.OWNER)
        project.save_to_db(project_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user12344"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        delete_project_controller(project_db, job_db, project.get_id(), auth_context_processor)

        self.assertRaises(KeyError, DBObject.load_from_db, Project, project.get_id(), project_db)
        self.assertRaises(KeyError, DBObject.load_from_db, Job, job.get_id(), job_db)

    def test_fail_project_nonexistant(self):
        pass

    def test_fail_device_not_authorized(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        project = self._build_default_project()
        job = self._build_default_job()
        project.create_job_path("2345")
        project.add_or_update_member("user12344", ProjectPrivilegeTypesEnum.OWNER)
        project.save_to_db(project_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "user12344"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, delete_project_controller, project_db, job_db, project.get_id(), auth_context_processor)

    def test_fail_not_authorized_to_access_project(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        project = self._build_default_project()
        job = self._build_default_job()
        project.create_job_path("2345")
        project.add_or_update_member("user12344", ProjectPrivilegeTypesEnum.OWNER)
        project.save_to_db(project_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user123445"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, delete_project_controller, project_db, job_db, project.get_id(), auth_context_processor)
