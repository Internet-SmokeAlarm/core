from dependencies.python.fmlaas.controller.create_experiment import \
    CreateExperimentController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsUser)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import (DBObject, Project,
                                              ProjectPrivilegeTypesEnum)
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class CreateExperimentControllerTestCase(AbstractTestCase):

    def test_pass(self):
        db = InMemoryDBInterface()

        project = self._build_simple_project()
        project.save_to_db(db)

        exp, _ = self._build_simple_experiment("1")

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = CreateExperimentController(db,
                                                project.id,
                                                exp.name,
                                                exp.description,
                                                exp.configuration,
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
        new_experiment = controller.execute()
        updated_project = DBObject.load_from_db(Project, project.id, db)
        self.assertTrue(updated_project.contains_experiment(new_experiment.id))
