from dependencies.python.fmlaas.controller.cancel_job import \
    CancelJobController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsUser)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import (DBObject, Project,
                                              ProjectPrivilegeTypesEnum)
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class CancelJobControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()
        experiment, _ = self._build_simple_experiment("1")
        job = self._build_simple_job()

        experiment.add_or_update_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        CancelJobController(
            project_db,
            project.id,
            experiment.id,
            job.id,
            auth_context).execute()

        db_project = DBObject.load_from_db(
            Project, project.id, project_db)

        self.assertTrue(job.id not in db_project.get_active_jobs())
        self.assertEqual(0, len(db_project.get_active_jobs()))
        self.assertTrue(db_project.get_experiment(experiment.id).get_job(job.id).is_cancelled())

    def test_get_auth_conditions_pass(self):
        project_db = InMemoryDBInterface()

        project = self._build_simple_project()
        experiment, _ = self._build_simple_experiment("1")
        job = self._build_simple_job()

        experiment.add_or_update_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = CancelJobController(project_db,
                                         project.id,
                                         experiment.id,
                                         job.id,
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
