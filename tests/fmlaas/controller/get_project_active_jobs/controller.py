from dependencies.python.fmlaas.model.device_factory import DeviceFactory
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
        experiment, _ = self._build_simple_experiment("1")
        job = self._build_simple_job()

        experiment.add_or_update_job(job)
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
        active_jobs = controller.execute()
        correct_active_jobs = [
            {
                "experiment_id": experiment.id,
                "job_id": job.id
            }
        ]
        self.assertEqual(correct_active_jobs, active_jobs)
    
    def test_pass_device(self):
        """
        Verifies that only the jobs that contain the specific device are returned
        """
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()

        device = DeviceFactory.create_device("12344")
        project.add_device(device)

        job_1 = self._build_simple_job()
        job_2 = self._build_simple_job("2", ["12345", "23456", "34567"])
        job_3 = self._build_simple_job("1")

        experiment_1, _ = self._build_simple_experiment("1")
        experiment_1.add_or_update_job(job_1)
        experiment_1.add_or_update_job(job_2)

        experiment_2, _ = self._build_simple_experiment("2")
        experiment_2.add_or_update_job(job_3)

        project.add_or_update_experiment(experiment_1)
        project.add_or_update_experiment(experiment_2)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)

        active_jobs = GetProjectActiveJobsController(project_db,
                                                     project.id,
                                                     auth_context).execute()
        correct_active_jobs = [
            {
                "experiment_id": experiment_1.id,
                "job_id": job_1.id
            },
            {
                "experiment_id": experiment_2.id,
                "job_id": job_3.id
            }
        ]
        self.assertEqual(correct_active_jobs, active_jobs)

        # Test updating to verify that job 2 is not included in active IDs
        job_1.cancel()
        experiment_1.add_or_update_job(job_1)
        project.add_or_update_experiment(experiment_1)

        active_jobs = GetProjectActiveJobsController(project_db,
                                                     project.id,
                                                     auth_context).execute()
        correct_active_jobs = [
            {
                "experiment_id": experiment_2.id,
                "job_id": job_3.id
            }
        ]
        self.assertEqual(correct_active_jobs, active_jobs)
