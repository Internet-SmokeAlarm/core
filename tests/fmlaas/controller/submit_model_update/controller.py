import unittest

from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.controller.submit_model_update import SubmitModelUpdateController
from dependencies.python.fmlaas.controller.utils.auth.conditions import IsDevice
from dependencies.python.fmlaas.controller.utils.auth.conditions import ProjectContainsJob
from dependencies.python.fmlaas.controller.utils.auth.conditions import JobContainsDevice
from dependencies.python.fmlaas.request_processor import AuthContextProcessor
from ..abstract_testcase import AbstractTestCase


class SubmitModelUpdateControllerTestCase(AbstractTestCase):

    def test_pass(self):
        project_db_ = InMemoryDBInterface()
        job_db_ = InMemoryDBInterface()

        job = self._build_simple_job()
        job.save_to_db(job_db_)

        project = self._build_simple_project()

        job_sequence = self._build_simple_job_sequence()
        job_sequence.id = "job_sequence_id_1"
        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        project.save_to_db(project_db_)

        auth_json = {
            "authentication_type": "DEVICE",
            "entity_id": "12344"
        }
        auth_context = AuthContextProcessor(auth_json)
        can_submit_model_to_job, presigned_url = SubmitModelUpdateController(project_db_,
                                                                             job_db_,
                                                                             project.get_id(),
                                                                             job.get_id(),
                                                                             auth_context).execute()
        self.assertTrue(can_submit_model_to_job)
        self.assertIsNotNone(presigned_url)
        self.assertTrue("device_models" in presigned_url["fields"]["key"])

    def test_load_data_pass(self):
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
        controller = SubmitModelUpdateController(project_db_,
                                                 job_db_,
                                                 project.get_id(),
                                                 job.get_id(),
                                                 auth_context)
        controller.load_data()

        self.assertEqual(controller.job, job)
        self.assertEqual(controller.project, project)

    def test_get_auth_conditions_pass(self):
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
        controller = SubmitModelUpdateController(project_db_,
                                                 job_db_,
                                                 project.get_id(),
                                                 job.get_id(),
                                                 auth_context)
        controller.load_data()
        auth_conditions = controller.get_auth_conditions()

        self.assertEqual(len(auth_conditions), 1)

        self.assertEqual(len(auth_conditions[0]), 3)
        self.assertEqual(auth_conditions[0][0], IsDevice())
        self.assertEqual(auth_conditions[0][1], ProjectContainsJob(project, job))
        self.assertEqual(auth_conditions[0][2], JobContainsDevice(job))
