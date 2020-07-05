from ..abstract_testcase import AbstractTestCase
from dependencies.python.fmlaas.controller.get_experiment import GetExperimentController
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions import HasProjectPermissions


class GetExperimentControllerTestCase(AbstractTestCase):

    def test_execute_pass(self):
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

        new_experiment = GetExperimentController(db, project.get_id(), experiment.id, auth_context).execute()

        self.assertEqual(experiment, new_experiment)

    def test_load_data_pass(self):
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

        controller = GetExperimentController(db, project.get_id(), experiment.id, auth_context)
        controller.load_data()

        self.assertEqual(controller.project, project)

    def test_get_auth_conditions_pass(self):
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

        controller = GetExperimentController(db, project.get_id(), experiment.id, auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()

        correct_auth_conditions = [
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_ONLY)
            ]
        ]

        self.assertEqual(auth_conditions, correct_auth_conditions)
