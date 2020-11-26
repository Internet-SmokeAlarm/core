from dependencies.python.fmlaas.controller.delete_project import \
    DeleteProjectController
from dependencies.python.fmlaas.controller.utils.auth.conditions import (
    HasProjectPermissions, IsUser)
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.model import (DBObject, ExperimentFactory, Job,
                                              Project,
                                              ProjectPrivilegeTypesEnum)
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

from ..abstract_testcase import AbstractTestCase


class DeleteProjectControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        project = self._build_simple_project()
        job = self._build_simple_job()
        experiment = ExperimentFactory.create_experiment("slksdklsdsdfsf",
                                                         "test_name")

        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = DeleteProjectController(project_db,
                                             job_db,
                                             project.id,
                                             auth_context)

        # Auth conditions
        auth_conditions = controller.get_auth_conditions()
        correct_auth_conditions = [
            [
                IsUser(),
                HasProjectPermissions(project, ProjectPrivilegeTypesEnum.ADMIN)
            ]
        ]

        self.assertEqual(auth_conditions, correct_auth_conditions)

        # Execute
        controller.execute()
        self.assertRaises(
            ValueError,
            DBObject.load_from_db,
            Job,
            job.id,
            job_db)
