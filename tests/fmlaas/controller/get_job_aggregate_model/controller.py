from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import ExperimentBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.get_job_aggregate_model import GetJobAggregateModelController
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions import HasProjectPermissions
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsJob
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsDevice
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsDevice
from ..abstract_testcase import AbstractTestCase


class GetJobAggregateModelControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.complete()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        builder = ExperimentBuilder()
        builder.id = "experiment_1"
        experiment = builder.build()

        experiment.add_job(job)
        experiment.proceed_to_next_job()
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        presigned_url = GetJobAggregateModelController(project_db_,
                                                       job_db_,
                                                       project.get_id(),
                                                       job.get_id(),
                                                       auth_context).execute()
        self.assertIsNotNone(presigned_url)

    def test_pass_not_complete(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        builder = ExperimentBuilder()
        builder.id = "experiment_1"
        experiment = builder.build()

        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

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
        self.assertRaises(ValueError, controller.execute)

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

        builder = ExperimentBuilder()
        builder.id = "experiment_1"
        experiment = builder.build()

        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

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
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_ONLY),
                ProjectContainsJob(project, job)
            ],
            [
                IsDevice(),
                ProjectContainsJob(project, job),
                ProjectContainsDevice(project)
            ]
        ]

        self.assertEqual(auth_conditions, correct_auth_conditions)
