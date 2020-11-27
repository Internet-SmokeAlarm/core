from dependencies.python.fmlaas.controller.start_job import StartJobController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsUser)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.device_selection import RandomDeviceSelector
from dependencies.python.fmlaas.model import (DBObject,
                                              DeviceSelectionStrategy,
                                              JobConfiguration, Project,
                                              ProjectPrivilegeTypesEnum)
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class StartJobControllerTestCase(AbstractTestCase):

    def test_get_device_selector_auth_cond_pass(self):
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()

        job = self._build_simple_job()

        experiment, _ = self._build_simple_experiment("1")
        experiment.add_or_update_job(job)

        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        job_config = JobConfiguration(1, 0, DeviceSelectionStrategy.RANDOM, [])

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = StartJobController(project_db,
                                        project.id,
                                        experiment.id, 
                                        job_config,
                                        auth_context)
        
        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)

        # Device Selector
        device_selector = controller.get_device_selector()
        self.assertEqual(device_selector.__class__, RandomDeviceSelector)

    def test_pass(self):
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()

        job = self._build_simple_job()

        experiment, _ = self._build_simple_experiment("1")
        experiment.add_or_update_job(job)

        job.cancel()
        experiment.add_or_update_job(job)

        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        job_config = JobConfiguration(1, 0, DeviceSelectionStrategy.RANDOM, [])

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        new_job = StartJobController(project_db,
                                     project.id,
                                     experiment.id,
                                     job_config,
                                     auth_context).execute()
        new_job_2 = StartJobController(project_db,
                                       project.id,
                                       experiment.id,
                                       job_config,
                                       auth_context).execute()
        new_job_3 = StartJobController(project_db,
                                       project.id,
                                       experiment.id,
                                       job_config,
                                       auth_context).execute()
        new_job_4 = StartJobController(project_db,
                                       project.id,
                                       experiment.id,
                                       job_config,
                                       auth_context).execute()
        
        updated_project = DBObject.load_from_db(
            Project, project.id, project_db)
        
        self.assertEqual(job.end_model, new_job.start_model)
        self.assertEqual(updated_project.get_active_jobs(), [new_job.id])
        self.assertTrue(updated_project.contains_job(new_job.id))
        self.assertTrue(updated_project.contains_job(new_job_2.id))
        self.assertTrue(updated_project.contains_job(new_job_3.id))
        self.assertTrue(updated_project.contains_job(new_job_4.id))

    def test_fail_no_devices(self):
        project_db = InMemoryDBInterface()
        
        project = self._build_simple_project()

        job = self._build_simple_job()

        experiment, _ = self._build_simple_experiment("1")
        experiment.add_or_update_job(job)

        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        job_config = JobConfiguration(5, 0, DeviceSelectionStrategy.RANDOM, [])

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertRaises(
            ValueError,
            StartJobController(project_db,
                               project.id,
                               experiment.id,
                               job_config,
                               auth_context).execute)
