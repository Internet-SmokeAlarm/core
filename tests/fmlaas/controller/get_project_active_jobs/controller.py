from dependencies.python.fmlaas.controller.get_project_active_jobs import GetProjectActiveJobsController
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsReadOnlyProjectEntity
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.model import JobStatus
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import JobSequenceBuilder
from dependencies.python.fmlaas.model import JobBuilder
from ..abstract_controller_testcase import AbstractControllerTestCase


class GetProjectActiveJobIdsControllerTestCase(AbstractControllerTestCase):

    def _build_default_project(self):
        project_builder = ProjectBuilder()
        project_builder.set_id("test_id")
        project_builder.set_name("test_name")

        project = project_builder.build()
        project.add_device("12344")
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.OWNER)

        job_sequence_builder = JobSequenceBuilder()
        job_sequence_builder.id = "sequence_id_1"
        job_sequence = job_sequence_builder.build()

        job_builder = JobBuilder()
        job_builder.set_id("1234432414")
        job_builder.set_project_id("fl_project_123123")
        configuration = JobConfiguration(50, 0, "RANDOM", [])
        job_builder.set_configuration(configuration.to_json())
        job_builder.set_job_sequence_id("sequence_id_1")
        job = job_builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        return project

    def test_pass(self):
        db_ = InMemoryDBInterface()
        project = self._build_default_project()
        project.save_to_db(db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        current_job_id = GetProjectActiveJobsController(
            db_, project.get_id(), auth_context).execute()
        self.assertEqual("1234432414", current_job_id[0])

    def test_pass_2(self):
        db_ = InMemoryDBInterface()
        project = self._build_default_project()
        project.save_to_db(db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        current_job_id_2 = GetProjectActiveJobsController(
            db_, project.get_id(), auth_context).execute()
        self.assertEqual("1234432414", current_job_id_2[0])

    def test_load_data_pass(self):
        db_ = InMemoryDBInterface()
        project = self._build_default_project()
        project.save_to_db(db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = GetProjectActiveJobsController(db_,
                                                    project.get_id(),
                                                    auth_context)
        controller.load_data()

        self.assertEqual(controller.project, project)

    def test_get_auth_conditions_pass(self):
        db_ = InMemoryDBInterface()
        project = self._build_default_project()
        project.save_to_db(db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = GetProjectActiveJobsController(db_,
                                                    project.get_id(),
                                                    auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()[0]

        self.assertEqual(len(auth_conditions), 1)
        self.assertEqual(auth_conditions[0], IsReadOnlyProjectEntity(project))
