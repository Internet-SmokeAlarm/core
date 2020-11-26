from dependencies.python.fmlaas.controller.start_job import StartJobController
from dependencies.python.fmlaas.controller.utils.auth.conditions.has_project_permissions import \
    HasProjectPermissions
from dependencies.python.fmlaas.controller.utils.auth.conditions.is_user import \
    IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions.project_contains_experiment import \
    ProjectContainsExperiment
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.device_selection import RandomDeviceSelector
from dependencies.python.fmlaas.model import (DBObject, Job, JobConfiguration,
                                              Project,
                                              ProjectPrivilegeTypesEnum)
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class StartJobControllerTestCase(AbstractTestCase):

    def test_get_device_selector_auth_cond_pass(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db)

        project = self._build_simple_project()
        experiment = self._build_simple_experiment()
        experiment.current_model = job.start_model
        experiment.start_model = job.start_model

        experiment.add_job(job)
        experiment.proceed_to_next_job()
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        job_config = JobConfiguration(1, 0, "RANDOM", [])

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = StartJobController(job_db,
                                        project_db,
                                        project.id,
                                        experiment.id, 
                                        job_config,
                                        auth_context)
        
        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_WRITE),
                ProjectContainsExperiment(project, experiment.id)
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)

        # Device Selector
        device_selector = controller.get_device_selector()
        self.assertEqual(device_selector.__class__, RandomDeviceSelector)

    def test_pass_1(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db)

        project = self._build_simple_project()
        experiment = self._build_simple_experiment()
        experiment.current_model = job.start_model
        experiment.start_model = job.start_model

        experiment.add_job(job)
        experiment.proceed_to_next_job()
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        job_config = JobConfiguration(1, 0, "RANDOM", [])

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        new_job = StartJobController(job_db,
                                     project_db,
                                     project.id,
                                     experiment.id,
                                     job_config,
                                     auth_context).execute()
        
        new_job = DBObject.load_from_db(Job, new_job.id, job_db)
        updated_project = DBObject.load_from_db(
            Project, project.id, project_db)

        self.assertEqual(new_job.devices, ["12344"])

        self.assertEqual(updated_project.get_active_jobs(), [job.id])
        self.assertTrue(updated_project.contains_job(new_job.id))

    def test_pass_2(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.cancel()
        job.save_to_db(job_db)

        project = self._build_simple_project()

        experiment = self._build_simple_experiment()
        experiment.current_model = job.start_model
        experiment.start_model = job.start_model

        experiment.add_job(job)
        experiment.proceed_to_next_job()
        experiment.proceed_to_next_job()
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        job_config = JobConfiguration(1, 0, "RANDOM", [])

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        new_job = StartJobController(job_db,
                                     project_db,
                                     project.id,
                                     experiment.id,
                                     job_config,
                                     auth_context).execute()
        
        new_job = DBObject.load_from_db(Job, new_job.id, job_db)
        updated_project = DBObject.load_from_db(
            Project, project.id, project_db)

        self.assertEqual(job.end_model.to_json(), new_job.start_model.to_json())
        self.assertEqual(updated_project.get_active_jobs(), [new_job.id])
        self.assertTrue(updated_project.contains_job(new_job.id))

    def test_pass_3(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.cancel()
        job.save_to_db(job_db)

        project = self._build_simple_project()

        experiment = self._build_simple_experiment()
        experiment.current_model = job.start_model
        experiment.start_model = job.start_model

        experiment.add_job(job)
        experiment.proceed_to_next_job()
        experiment.proceed_to_next_job()
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        job_config = JobConfiguration(1, 0, "RANDOM", [])

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        new_job = StartJobController(job_db,
                                     project_db,
                                     project.id,
                                     experiment.id,
                                     job_config,
                                     auth_context).execute()
        new_job_2 = StartJobController(job_db,
                                       project_db,
                                       project.id,
                                       experiment.id,
                                       job_config,
                                       auth_context).execute()
        new_job_3 = StartJobController(job_db,
                                       project_db,
                                       project.id,
                                       experiment.id,
                                       job_config,
                                       auth_context).execute()
        new_job_4 = StartJobController(job_db,
                                       project_db,
                                       project.id,
                                       experiment.id,
                                       job_config,
                                       auth_context).execute()
        
        updated_project = DBObject.load_from_db(
            Project, project.id, project_db)

        print(f"exp active jobs: {experiment.jobs}")
        self.assertEqual(job.end_model, new_job.start_model)
        self.assertEqual(updated_project.get_active_jobs(), [new_job.id])
        self.assertTrue(updated_project.contains_job(new_job.id))
        self.assertTrue(updated_project.contains_job(new_job_2.id))
        self.assertTrue(updated_project.contains_job(new_job_3.id))
        self.assertTrue(updated_project.contains_job(new_job_4.id))

    def test_fail_no_devices(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db)

        project = self._build_simple_project()

        experiment = self._build_simple_experiment()
        experiment.current_model = job.start_model
        experiment.start_model = job.start_model

        experiment.add_job(job)
        experiment.proceed_to_next_job()
        experiment.proceed_to_next_job()
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        job_config = JobConfiguration(5, 0, "RANDOM", [])

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        self.assertRaises(
            ValueError,
            StartJobController(job_db,
                               project_db,
                               project.id,
                               experiment.id,
                               job_config,
                               auth_context).execute)
