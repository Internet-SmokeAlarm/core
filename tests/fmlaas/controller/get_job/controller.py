from dependencies.python.fmlaas.controller.get_job import GetJobController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsUser, ProjectContainsJob)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class GetJobControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        experiment = self._build_simple_experiment()
        experiment.add_job(job)

        project = self._build_simple_project()
        project.add_or_update_experiment(experiment)
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = GetJobController(project_db_,
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
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)

        # Execute
        retrieved_job = controller.execute()
        self.assertEqual(retrieved_job.id, job.id)