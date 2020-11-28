from dependencies.python.fmlaas.controller.submit_experiment_start_model import \
    SubmitExperimentStartModelController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsUser)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class SubmitExperimentStartModelControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()
        experiment, _ = self._build_simple_experiment("1")

        # By default, we add parameters to the experiment. We want to remove
        #   those parameters so that we can set them again in the test.
        experiment.configuration._parameters = dict()
        
        project.add_or_update_experiment(experiment)
        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = SubmitExperimentStartModelController(project_db,
                                                          project.id,
                                                          experiment.id,
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

        # Execute
        can_submit_start_model, presigned_url = controller.execute()
        self.assertTrue(can_submit_start_model)
        self.assertIsNotNone(presigned_url)
