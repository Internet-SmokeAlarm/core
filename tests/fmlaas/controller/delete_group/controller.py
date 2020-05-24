import unittest

from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.controller.delete_group import delete_group_controller
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

class DeleteGroupControllerTestCase(unittest.TestCase):

    def _build_default_group(self):
        group_builder = GroupBuilder()
        group_builder.set_id("test_id")
        group_builder.set_name("test_name")

        return group_builder.build()

    def _build_default_job(self):
        job_builder = JobBuilder()
        job_builder.set_id("2345")
        job_builder.set_parent_group_id("test_id")
        configuration = JobConfiguration(1, 0, "RANDOM", [])
        job_builder.set_configuration(configuration.to_json())
        job_builder.set_devices(["3456"])
        job_builder.set_start_model(Model("1234", "1234/1234", "123211").to_json())

        return job_builder.build()

    def test_pass_1(self):
        group_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        group = self._build_default_group()
        job = self._build_default_job()
        group.create_job_path("2345")
        group.add_or_update_member("user12344", GroupPrivilegeTypesEnum.OWNER)
        group.save_to_db(group_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user12344"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        delete_group_controller(group_db, job_db, group.get_id(), auth_context_processor)

        self.assertRaises(KeyError, DBObject.load_from_db, FLGroup, group.get_id(), group_db)
        self.assertRaises(KeyError, DBObject.load_from_db, Job, job.get_id(), job_db)

    def test_fail_group_nonexistant(self):
        pass

    def test_fail_device_not_authorized(self):
        group_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        group = self._build_default_group()
        job = self._build_default_job()
        group.create_job_path("2345")
        group.add_or_update_member("user12344", GroupPrivilegeTypesEnum.OWNER)
        group.save_to_db(group_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "user12344"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, delete_group_controller, group_db, job_db, group.get_id(), auth_context_processor)

    def test_fail_not_authorized_to_access_group(self):
        group_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        group = self._build_default_group()
        job = self._build_default_job()
        group.create_job_path("2345")
        group.add_or_update_member("user12344", GroupPrivilegeTypesEnum.OWNER)
        group.save_to_db(group_db)
        job.save_to_db(job_db)

        auth_json = {
            "authentication_type" : "JWT",
            "entity_id" : "user123445"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, delete_group_controller, group_db, job_db, group.get_id(), auth_context_processor)
