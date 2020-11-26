from dependencies.python.fmlaas.controller.get_project_active_jobs import \
    GetProjectActiveJobsController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsDevice, IsUser, ProjectContainsDevice)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class GetProjectActiveJobIdsControllerTestCase(AbstractTestCase):

    def test_pass(self):
        db_ = InMemoryDBInterface()

        project = self._build_simple_project()
        experiment = self._build_simple_experiment()
        job = self._build_simple_job()

        experiment.add_job(job)
        experiment.proceed_to_next_job()
        project.add_or_update_experiment(experiment)

        project.save_to_db(db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = GetProjectActiveJobsController(db_,
                                                    project.id,
                                                    auth_context)

        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ],
            [
                IsDevice(),
                ProjectContainsDevice(project)
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)

        # Execute
        current_job_ids = controller.execute()
        self.assertEqual([job.id], current_job_ids)
