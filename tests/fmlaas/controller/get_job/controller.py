from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.get_job import GetJobController
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions import HasProjectPermissions
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsJob
from ..abstract_controller_testcase import AbstractControllerTestCase


class GetJobControllerTestCase(AbstractControllerTestCase):

    def test_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        job_sequence = self._build_simple_job_sequence()
        job_sequence.add_job(job)

        project = self._build_simple_project()
        project.add_or_update_job_sequence(job_sequence)
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        retrieved_job = GetJobController(
            project_db_,
            job_db_,
            project.get_id(),
            job.get_id(),
            auth_context).execute()
        self.assertEqual(retrieved_job.get_id(), job.get_id())

    def test_load_data_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = GetJobController(project_db_,
                                      job_db_,
                                      project.get_id(),
                                      job.get_id(),
                                      auth_context)
        controller.load_data()

        self.assertEqual(controller.project, project)
        self.assertEqual(controller.job, job)

    def test_get_auth_conditions_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = GetJobController(project_db_,
                                      job_db_,
                                      project.get_id(),
                                      job.get_id(),
                                      auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()

        self.assertEqual(len(auth_conditions), 3)
        self.assertEqual(auth_conditions[0], IsUser())
        self.assertEqual(auth_conditions[1], HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_ONLY))
        self.assertEqual(auth_conditions[2], ProjectContainsJob(project, job))
