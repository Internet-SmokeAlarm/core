from dependencies.python.fmlaas.controller.submit_model_update import \
    SubmitModelUpdateController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    IsDevice, JobContainsDevice, ProjectContainsJob)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class SubmitModelUpdateControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        experiment = self._build_simple_experiment()
        experiment.add_job(job)
        experiment.start_model = job.start_model
        experiment.current_model = job.start_model
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = SubmitModelUpdateController(project_db_,
                                                 job_db_,
                                                 project.id,
                                                 job.id,
                                                 auth_context)
        
        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsDevice(),
                ProjectContainsJob(project, job),
                JobContainsDevice(job)
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)
        
        # Execute
        can_submit_model_to_job, presigned_url = controller.execute()
        self.assertTrue(can_submit_model_to_job)
        self.assertIsNotNone(presigned_url)
        self.assertTrue("device_models" in presigned_url["fields"]["key"])
