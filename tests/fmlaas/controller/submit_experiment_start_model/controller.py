import unittest

from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.submit_experiment_start_model import SubmitExperimentStartModelController
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions import HasProjectPermissions
from ..abstract_testcase import AbstractTestCase


class SubmitExperimentStartModelControllerTestCase(AbstractTestCase):

    def test_execute_pass(self):
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()
        experiment = self._build_simple_experiment()
        project.add_or_update_experiment(experiment)
        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        can_submit_start_model, presigned_url = SubmitExperimentStartModelController(project_db, project.get_id(), experiment.id, auth_context).execute()

        self.assertTrue(can_submit_start_model)
        self.assertIsNotNone(presigned_url)

    def test_get_auth_conditions_pass(self):
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()
        experiment = self._build_simple_experiment()
        project.add_or_update_experiment(experiment)
        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = SubmitExperimentStartModelController(project_db, project.get_id(), experiment.id, auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()

        correct_auth_conditions = [
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_WRITE)
            ]
        ]

        self.assertEqual(auth_conditions, correct_auth_conditions)

    def test_load_data_pass(self):
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()
        experiment = self._build_simple_experiment()
        project.add_or_update_experiment(experiment)
        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = SubmitExperimentStartModelController(project_db, project.get_id(), experiment.id, auth_context)
        controller.load_data()

        self.assertEqual(project, controller.project)
        self.assertEqual(experiment, controller.experiment)
