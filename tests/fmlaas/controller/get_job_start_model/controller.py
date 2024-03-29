from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import ExperimentBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.get_job_start_model import GetJobStartModelController
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsJob
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions import HasProjectPermissions
from dependencies.python.fmlaas.controller.utils.auth.conditions import JobContainsDevice
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsDevice
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from ..abstract_testcase import AbstractTestCase


class GetJobStartModelControllerTestCase(AbstractTestCase):

    def test_pass_1(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        builder = ExperimentBuilder()
        builder.id = "experiment_1"
        experiment = builder.build()

        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        presigned_url = GetJobStartModelController(project_db_,
                                                   job_db_,
                                                   job.get_id(),
                                                   auth_context).execute()
        self.assertIsNotNone(presigned_url)

    def test_pass_2(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        builder = ExperimentBuilder()
        builder.id = "experiment_1"
        experiment = builder.build()

        experiment.add_job(job)
        project.add_or_update_experiment(experiment)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        presigned_url = GetJobStartModelController(project_db_,
                                                   job_db_,
                                                   job.get_id(),
                                                   auth_context).execute()
        self.assertIsNotNone(presigned_url)

    def test_load_data(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = GetJobStartModelController(project_db_,
                                                job_db_,
                                                job.get_id(),
                                                auth_context)
        controller.load_data()

        self.assertEqual(controller.project, project)
        self.assertEqual(controller.job, job)

    def test_get_auth_conditions(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()
        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = GetJobStartModelController(project_db_,
                                                job_db_,
                                                job.get_id(),
                                                auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()

        self.assertEqual(len(auth_conditions), 2)

        self.assertEqual(len(auth_conditions[1]), 3)
        self.assertEqual(auth_conditions[1][0], IsUser())
        self.assertEqual(auth_conditions[1][1], HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_ONLY))
        self.assertEqual(auth_conditions[1][2], ProjectContainsJob(project, job))

        self.assertEqual(len(auth_conditions[0]), 2)
        self.assertEqual(auth_conditions[0][0], IsDevice())
        self.assertEqual(auth_conditions[0][1], JobContainsDevice(job))
