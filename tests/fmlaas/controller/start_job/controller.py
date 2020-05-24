import unittest

from dependencies.python.fmlaas.device_selection import RandomDeviceSelector
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum
from dependencies.python.fmlaas.exception import RequestForbiddenException
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.start_job import get_device_selector
from dependencies.python.fmlaas.controller.start_job import create_job
from dependencies.python.fmlaas.controller.start_job import start_job_controller
from dependencies.python.fmlaas.request_processor import AuthContextProcessor

class StartJobControllerTestCase(unittest.TestCase):

    def test_get_device_selector_pass(self):
        device_selector = get_device_selector(JobConfiguration(5, 0, "RANDOM", []))

        self.assertEqual(device_selector.__class__, RandomDeviceSelector)

    def test_create_job_pass(self):
        devices = ["123", "234", "345", "3456"]
        job_config = JobConfiguration(4, 0, "RANDOM", [])

        new_job = create_job(devices, "test_id123", job_config)

        self.assertIsNotNone(new_job.get_id())
        self.assertEqual(new_job.get_devices(), devices)
        self.assertEqual(new_job.get_parent_group_id(), "test_id123")
        self.assertEqual(job_config.to_json(), new_job.get_configuration().to_json())

    def test_start_job_controller_pass_1(self):
        group_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_parent_group_id("test_id")
        job_builder.set_configuration(JobConfiguration(1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()

        group.create_job_path(job.get_id())
        group.add_current_job_id(job.get_id())

        job.save_to_db(job_db)
        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        new_job_id = start_job_controller(job_db, group_db, group.get_id(), JobConfiguration(1, 0, "RANDOM", []), job.get_id(), auth_context_processor)
        new_job = DBObject.load_from_db(Job, new_job_id, job_db)

        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)

        self.assertEqual(updated_group.get_current_job_ids(), [job.get_id()])
        self.assertTrue(updated_group.contains_job(new_job_id))

    def test_start_job_controller_pass_2(self):
        group_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)

        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        new_job_id = start_job_controller(job_db, group_db, group.get_id(), JobConfiguration(1, 0, "RANDOM", []), "", auth_context_processor)
        new_job = DBObject.load_from_db(Job, new_job_id, job_db)
        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)

        self.assertEqual(new_job.get_devices(), ["34553"])

        self.assertEqual(updated_group.get_current_job_ids(), [new_job_id])
        self.assertEqual(updated_group.get_job_paths(), [[new_job_id]])
        self.assertTrue(updated_group.contains_job(new_job_id))

    def test_start_job_controller_pass_3(self):
        group_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_parent_group_id("test_id")
        job_builder.set_configuration(JobConfiguration(1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()
        job.cancel()

        group.create_job_path(job.get_id())

        job.save_to_db(job_db)
        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        new_job_id = start_job_controller(job_db, group_db, group.get_id(), JobConfiguration(1, 0, "RANDOM", []), job.get_id(), auth_context_processor)
        new_job = DBObject.load_from_db(Job, new_job_id, job_db)

        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)

        self.assertEqual(job.get_end_model().to_json(), new_job.get_start_model().to_json())
        self.assertEqual(updated_group.get_current_job_ids(), [new_job_id])
        self.assertTrue(updated_group.contains_job(new_job_id))

    def test_start_job_controller_pass_4(self):
        group_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_parent_group_id("test_id")
        job_builder.set_configuration(JobConfiguration(1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(Model("12312414", "12312414/start_model", "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()

        group.create_job_path(job.get_id())

        job.save_to_db(job_db)
        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        new_job_id = start_job_controller(job_db, group_db, group.get_id(), JobConfiguration(1, 0, "RANDOM", []), job.get_id(), auth_context_processor)
        new_job_id_2 = start_job_controller(job_db, group_db, group.get_id(), JobConfiguration(1, 0, "RANDOM", []), new_job_id, auth_context_processor)
        new_job_id_3 = start_job_controller(job_db, group_db, group.get_id(), JobConfiguration(1, 0, "RANDOM", []), new_job_id_2, auth_context_processor)
        new_job_id_4 = start_job_controller(job_db, group_db, group.get_id(), JobConfiguration(1, 0, "RANDOM", []), new_job_id_3, auth_context_processor)
        new_job = DBObject.load_from_db(Job, new_job_id, job_db)

        updated_group = DBObject.load_from_db(FLGroup, group.get_id(), group_db)

        self.assertEqual(job.get_end_model().to_json(), new_job.get_start_model().to_json())
        self.assertEqual(updated_group.get_current_job_ids(), [new_job_id])
        self.assertTrue(updated_group.contains_job(new_job_id))

    def test_start_job_controller_fail_no_devices(self):
        group_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)

        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_12345"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(ValueError, start_job_controller, job_db, group_db, group.get_id(), JobConfiguration(1, 0, "RANDOM", []), "", auth_context_processor)

    def test_start_job_controller_fail(self):
        group_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)
        group.add_or_update_member("user_123456", GroupPrivilegeTypesEnum.READ_ONLY)

        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_123456"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, start_job_controller, job_db, group_db, group.get_id(), JobConfiguration(1, 0, "RANDOM", []), None, auth_context_processor)

    def test_start_job_controller_fail_2(self):
        group_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)
        group.add_or_update_member("user_123456", GroupPrivilegeTypesEnum.READ_ONLY)

        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "USER",
            "entity_id" : "user_1234567"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, start_job_controller, job_db, group_db, group.get_id(), JobConfiguration(1, 0, "RANDOM", []), None, auth_context_processor)

    def test_start_job_controller_fail_3(self):
        group_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = GroupBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices({"34553" : {"ID" : "34553", "registered_on" : "213123144.2342"}})
        group = builder.build()
        group.add_or_update_member("user_12345", GroupPrivilegeTypesEnum.ADMIN)
        group.add_or_update_member("user_123456", GroupPrivilegeTypesEnum.READ_ONLY)

        group.save_to_db(group_db)

        auth_json = {
            "authentication_type" : "DEVICE",
            "entity_id" : "34553"
        }
        auth_context_processor = AuthContextProcessor(auth_json)

        self.assertRaises(RequestForbiddenException, start_job_controller, job_db, group_db, group.get_id(), JobConfiguration(1, 0, "RANDOM", []), None, auth_context_processor)
