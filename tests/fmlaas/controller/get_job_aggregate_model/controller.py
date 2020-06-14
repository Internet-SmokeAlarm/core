from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobSequenceBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.get_job_aggregate_model import GetJobAggregateModelController
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions import HasProjectPermissions
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsJob
from ..abstract_testcase import AbstractTestCase


class GetJobAggregateModelControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.complete()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        builder = JobSequenceBuilder()
        builder.id = "job_sequence_1"
        job_sequence = builder.build()

        job_sequence.add_job(job)
        job_sequence.proceed_to_next_job()
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        is_job_complete, presigned_url = GetJobAggregateModelController(project_db_,
                                                                        job_db_,
                                                                        project.get_id(),
                                                                        job.get_id(),
                                                                        auth_context).execute()
        self.assertTrue(is_job_complete)
        self.assertIsNotNone(presigned_url)

    def test_pass_not_complete(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

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

        is_job_complete, presigned_url = GetJobAggregateModelController(project_db_,
                                                                        job_db_,
                                                                        project.get_id(),
                                                                        job.get_id(),
                                                                        auth_context).execute()
        self.assertFalse(is_job_complete)
        self.assertIsNone(presigned_url)

    def test_load_data_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.complete()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = GetJobAggregateModelController(project_db_,
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

        controller = GetJobAggregateModelController(project_db_,
                                                    job_db_,
                                                    project.get_id(),
                                                    job.get_id(),
                                                    auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()[0]

        self.assertEqual(len(auth_conditions), 3)
        self.assertEqual(auth_conditions[0], IsUser())
        self.assertEqual(auth_conditions[1], HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_ONLY))
        self.assertEqual(auth_conditions[2], ProjectContainsJob(project, job))
