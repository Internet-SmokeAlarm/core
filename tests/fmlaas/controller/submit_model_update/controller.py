from dependencies.python.fmlaas.controller.submit_model_update import \
    SubmitModelUpdateController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    IsDevice, JobContainsDevice)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class SubmitModelUpdateControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db_ = InMemoryDBInterface()

        job = self._build_simple_job()

        project = self._build_simple_project()

        experiment, _ = self._build_simple_experiment("1")
        experiment.add_or_update_job(job)

        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = SubmitModelUpdateController(project_db_,
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
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)
        
        # Execute
        can_submit_model_to_job, presigned_url = controller.execute()
        self.assertTrue(can_submit_model_to_job)
        self.assertIsNotNone(presigned_url)
        self.assertTrue("device_models" in presigned_url["fields"]["key"])
