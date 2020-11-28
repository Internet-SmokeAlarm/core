from dependencies.python.fmlaas.controller.get_job_start_model import \
    GetJobStartModelController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsDevice, IsUser, JobContainsDevice)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class GetJobStartModelControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db_ = InMemoryDBInterface()

        job = self._build_simple_job()

        project = self._build_simple_project()
        experiment, _ = self._build_simple_experiment("1")

        experiment.add_or_update_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = GetJobStartModelController(project_db_,
                                                project.id,
                                                experiment.id,
                                                job.id,
                                                auth_context)

        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsDevice(),
                JobContainsDevice(job)
            ],
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)

        # Execute
        presigned_url = controller.execute()
        self.assertIsNotNone(presigned_url)
