from dependencies.python.fmlaas.controller.get_experiment import \
    GetExperimentController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsUser)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class GetExperimentControllerTestCase(AbstractTestCase):

    def test_pass(self):
        db = InMemoryDBInterface()

        project = self._build_simple_project()
        experiment = self._build_simple_experiment()
        project.add_or_update_experiment(experiment)

        project.save_to_db(db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = GetExperimentController(db,
                                             project.id,
                                             experiment.id,
                                             auth_context)

        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ]
        ]
        self.assertEqual(auth_conditions, correct_auth_conditions)

        # Execute
        new_experiment = controller.execute()
        self.assertEqual(experiment, new_experiment)
