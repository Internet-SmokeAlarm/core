import unittest

from dependencies.python.fmlaas.controller.delete_project import DeleteProjectController
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions import HasProjectPermissions
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import ExperimentBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor


class DeleteProjectControllerTestCase(unittest.TestCase):

    def _build_default_project(self):
        project_builder = ProjectBuilder()
        project_builder.set_id("test_id")
        project_builder.set_name("test_name")

        return project_builder.build()

    def _build_default_job(self):
        job_builder = JobBuilder()
        job_builder.set_id("2345")
        job_builder.set_project_id("test_id")
        job_builder.set_experiment_id("test_id_2")
        configuration = JobConfiguration(1, 0, "RANDOM", [])
        job_builder.set_configuration(configuration.to_json())
        job_builder.set_devices(["3456"])
        job_builder.set_start_model(
            Model(
                "1234",
                "1234/1234",
                "123211").to_json())

        return job_builder.build()

    def test_load_data_pass(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        project = self._build_default_project()

        project.add_or_update_member(
            "user12344", ProjectPrivilegeTypesEnum.OWNER)
        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user12344"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = DeleteProjectController(project_db,
                                             job_db,
                                             project.get_id(),
                                             auth_context)
        controller.load_data()

        self.assertEqual(controller.project, project)

    def test_execute_pass(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        project = self._build_default_project()
        job = self._build_default_job()

        builder = ExperimentBuilder()
        builder.id = "dfaslkfskljf"
        experiment = builder.build()

        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        project.add_or_update_member(
            "user12344", ProjectPrivilegeTypesEnum.OWNER)
        project.save_to_db(project_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user12344"
        }
        auth_context = AuthContextProcessor(auth_json)

        DeleteProjectController(
            project_db,
            job_db,
            project.get_id(),
            auth_context).execute()

        self.assertRaises(
            ValueError,
            DBObject.load_from_db,
            Project,
            project.get_id(),
            project_db)
        self.assertRaises(
            ValueError,
            DBObject.load_from_db,
            Job,
            job.get_id(),
            job_db)

    def test_get_auth_conditions_pass(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        project = self._build_default_project()

        project.add_or_update_member(
            "user12344", ProjectPrivilegeTypesEnum.OWNER)
        project.save_to_db(project_db)

        auth_json = {
            "authentication_type": "JWT",
            "entity_id": "user123445"
        }
        auth_context = AuthContextProcessor(auth_json)

        controller = DeleteProjectController(project_db, job_db, project.get_id(), auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()[0]

        self.assertEqual(len(auth_conditions), 2)
        self.assertEqual(auth_conditions[0], IsUser())
        self.assertEqual(auth_conditions[1], HasProjectPermissions(project, ProjectPrivilegeTypesEnum.ADMIN))
