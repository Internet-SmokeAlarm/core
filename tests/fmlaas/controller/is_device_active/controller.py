from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobSequenceBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.is_device_active import IsDeviceActiveController
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsUser
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsDevice
from dependencies.python.fmlaas.controller.utils.auth.conditions import HasProjectPermissions
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsJob
from dependencies.python.fmlaas.controller.utils.auth.conditions import JobContainsDevice
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsEqualToAuthEntity
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from ..abstract_controller_testcase import AbstractControllerTestCase


class IsDeviceActiveControllerTestCase(AbstractControllerTestCase):

    def test_pass_device(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        builder = JobSequenceBuilder()
        builder.id = "test_job_sequence_1"
        job_sequence = builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        is_device_active = IsDeviceActiveController(project_db_,
                                                    job_db_,
                                                    project.get_id(),
                                                    job.get_id(),
                                                    "12344",
                                                    auth_context).execute()
        self.assertTrue(is_device_active)

    def test_pass_user(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        builder = JobSequenceBuilder()
        builder.id = "test_job_sequence_1"
        job_sequence = builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        is_device_active = IsDeviceActiveController(project_db_,
                                                    job_db_,
                                                    project.get_id(),
                                                    job.get_id(),
                                                    "12344",
                                                    auth_context).execute()
        self.assertTrue(is_device_active)

        is_device_active = IsDeviceActiveController(project_db_,
                                                    job_db_,
                                                    project.get_id(),
                                                    job.get_id(),
                                                    "123445",
                                                    auth_context).execute()
        self.assertFalse(is_device_active)

    def test_load_data_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        builder = JobSequenceBuilder()
        builder.id = "test_job_sequence_1"
        job_sequence = builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = IsDeviceActiveController(project_db_,
                                              job_db_,
                                              project.get_id(),
                                              job.get_id(),
                                              "123445",
                                              auth_context)
        controller.load_data()

        self.assertEqual(controller.project, project)
        self.assertEqual(controller.job, job)

    def test_get_auth_conditions_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        builder = JobSequenceBuilder()
        builder.id = "test_job_sequence_1"
        job_sequence = builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "USER",
            "entity_id": "user_12345"
        }
        auth_context = AuthContextProcessor(auth_json)
        controller = IsDeviceActiveController(project_db_,
                                              job_db_,
                                              project.get_id(),
                                              job.get_id(),
                                              "123445",
                                              auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()

        self.assertEqual(len(auth_conditions), 2)

        self.assertEqual(len(auth_conditions[0]), 3)
        self.assertEqual(auth_conditions[0][0], IsUser())
        self.assertEqual(auth_conditions[0][1], HasProjectPermissions(project, ProjectPrivilegeTypesEnum.READ_ONLY))
        self.assertEqual(auth_conditions[0][2], ProjectContainsJob(project, job))

        self.assertEqual(len(auth_conditions[1]), 4)
        self.assertEqual(auth_conditions[1][0], IsDevice())
        self.assertEqual(auth_conditions[1][1], JobContainsDevice(job))
        self.assertEqual(auth_conditions[1][2], ProjectContainsJob(project, job))
        self.assertEqual(auth_conditions[1][3], IsEqualToAuthEntity("123445"))
