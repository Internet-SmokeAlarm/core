from dependencies.python.fmlaas.controller.is_device_active import \
    IsDeviceActiveController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsDevice, IsEqualToAuthEntity, IsUser,
    JobContainsDevice, ProjectContainsJob)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class IsDeviceActiveControllerTestCase(AbstractTestCase):

    def test_pass(self):
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
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        is_device_active = IsDeviceActiveController(project_db_,
                                                    job_db_,
                                                    project.id,
                                                    job.id,
                                                    "12344",
                                                    auth_context).execute()
        self.assertTrue(is_device_active)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        is_device_active = IsDeviceActiveController(project_db_,
                                                    job_db_,
                                                    project.id,
                                                    job.id,
                                                    "12344",
                                                    auth_context).execute()
        self.assertTrue(is_device_active)

        is_device_active = IsDeviceActiveController(project_db_,
                                                    job_db_,
                                                    project.id,
                                                    job.id,
                                                    "123445",
                                                    auth_context).execute()
        self.assertFalse(is_device_active)

        controller = IsDeviceActiveController(project_db_,
                                              job_db_,
                                              project.id,
                                              job.id,
                                              "123445",
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
                JobContainsDevice(job),
                ProjectContainsJob(project, job),
                IsEqualToAuthEntity("123445")
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)
