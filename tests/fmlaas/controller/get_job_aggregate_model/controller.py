from dependencies.python.fmlaas.controller.get_job_aggregate_model import \
    GetJobAggregateModelController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsDevice, IsUser, ProjectContainsDevice,
    ProjectContainsJob)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class GetJobAggregateModelControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.complete()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        experiment = self._build_simple_experiment()
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
                                                       project.id,
                                                       job.id,
                                                       auth_context).execute()
        self.assertIsNotNone(presigned_url)

    def test_pass_not_complete(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        experiment = self._build_simple_experiment()
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
                                                    project.id,
                                                    job.id,
                                                    auth_context)

        # Auth conditions
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

        # Execute
        self.assertRaises(ValueError, controller.execute)
