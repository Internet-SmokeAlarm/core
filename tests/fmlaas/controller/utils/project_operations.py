from dependencies.python.fmlaas.device_selection import RandomDeviceSelector
from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobSequenceBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import Job
from dependencies.python.fmlaas.model import DBObject
from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas.database import InMemoryDBInterface
from dependencies.python.fmlaas.controller.utils import update_job_sequence
from dependencies.python.fmlaas.utils import get_epoch_time
from dependencies.python.fmlaas.model.termination_criteria import DurationTerminationCriteria
from dependencies.python.fmlaas.controller.utils import termination_check
from ..abstract_testcase import AbstractTestCase


class ProjectOperationsTestCase(AbstractTestCase):

    def test_update_job_sequence_pass(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)
        project.add_device("device_1")

        builder = JobSequenceBuilder()
        builder.id = "123dafasdf34sdfsdf"
        job_sequence = builder.build()

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
        job_builder.set_job_sequence_id("123dafasdf34sdfsdf")
        job_builder.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(
            Model(
                "12312414",
                "12312414/start_model",
                "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()

        job_sequence.add_job(job)
        project.add_or_update_job_sequence(job_sequence)

        job.save_to_db(job_db)
        project.save_to_db(project_db)

        update_job_sequence(job, job_db, project_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)

        self.assertEqual(updated_project.get_active_jobs(), [])
        self.assertTrue(updated_project.contains_job(job.get_id()))

    def test_update_job_sequence_pass_2(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        builder = JobSequenceBuilder()
        builder.id = "123dafasdf34sdfsdf"
        job_sequence = builder.build()
        job_sequence.current_model = Model(
            "12312414",
            "12312414/start_model",
            "123211")

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
        job_builder.set_job_sequence_id("123dafasdf34sdfsdf")
        job_builder.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(
            Model(
                "12312414",
                "12312414/start_model",
                "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()
        job.cancel()

        job_builder_2 = JobBuilder()
        job_builder_2.set_id("job_test_id_2")
        job_builder_2.set_project_id("test_id")
        job_builder_2.set_job_sequence_id("123dafasdf34sdfsdf")
        job_builder_2.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder_2.set_devices(["34553"])
        job_2 = job_builder_2.build()

        job_sequence.add_job(job)
        job_sequence.add_job(job_2)
        project.add_or_update_job_sequence(job_sequence)

        job.save_to_db(job_db)
        job_2.save_to_db(job_db)
        project.save_to_db(project_db)

        update_job_sequence(job, job_db, project_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)
        update_job_2 = DBObject.load_from_db(Job, job_2.get_id(), job_db)

        self.assertEqual(
            updated_project.get_active_jobs(), [
                job_2.get_id()])
        self.assertTrue(update_job_2.is_in_progress())
        self.assertEqual(
            job.get_end_model().to_json(),
            update_job_2.get_start_model().to_json())
        self.assertTrue(updated_project.contains_job(job.get_id()))
        self.assertTrue(updated_project.contains_job(job_2.get_id()))

    def test_update_job_sequence_pass_3(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        builder = JobSequenceBuilder()
        builder.id = "123dafasdf34sdfsdf"
        job_sequence = builder.build()
        job_sequence.current_model = Model(
            "12312414",
            "12312414/start_model",
            "123211")

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
        job_builder.set_job_sequence_id("123dafasdf34sdfsdf")
        job_builder.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(
            Model(
                "12312414",
                "12312414/start_model",
                "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()
        job.cancel()

        job_builder_2 = JobBuilder()
        job_builder_2.set_id("job_test_id_2")
        job_builder_2.set_project_id("test_id")
        job_builder_2.set_job_sequence_id("123dafasdf34sdfsdf")
        job_builder_2.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", [
                    DurationTerminationCriteria(
                        100, 5000.123).to_json()]).to_json())
        job_builder_2.set_devices(["34553"])
        job_2 = job_builder_2.build()

        job_sequence.add_job(job)
        job_sequence.add_job(job_2)
        project.add_or_update_job_sequence(job_sequence)

        job.save_to_db(job_db)
        job_2.save_to_db(job_db)
        project.save_to_db(project_db)

        self.assertTrue(job_2.should_terminate())

        update_job_sequence(job, job_db, project_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)
        update_job_2 = DBObject.load_from_db(Job, job_2.get_id(), job_db)

        self.assertEqual(
            updated_project.get_active_jobs(), [
                job_2.get_id()])
        self.assertTrue(update_job_2.is_in_progress())
        self.assertEqual(job.get_end_model(), update_job_2.get_start_model())
        self.assertTrue(updated_project.contains_job(job.get_id()))
        self.assertTrue(updated_project.contains_job(job_2.get_id()))
        self.assertFalse(update_job_2.should_terminate())

    def test_update_job_sequence_pass_4(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        builder = JobSequenceBuilder()
        builder.id = "123dafasdf34sdfsdf"
        job_sequence = builder.build()
        job_sequence.current_model = Model(
            "12312414",
            "12312414/start_model",
            "123211")

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
        job_builder.set_job_sequence_id("123dafasdf34sdfsdf")
        job_builder.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder.set_start_model(
            Model(
                "12312414",
                "12312414/start_model",
                "123211").to_json())
        job_builder.set_aggregate_model(
            Model(
                "12312414",
                "12312414/aggregate_model",
                "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()
        job.complete()

        job_builder_2 = JobBuilder()
        job_builder_2.set_id("job_test_id_2")
        job_builder_2.set_project_id("test_id")
        job_builder_2.set_job_sequence_id("123dafasdf34sdfsdf")
        job_builder_2.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder_2.set_devices(["34553"])
        job_2 = job_builder_2.build()

        job_sequence.add_job(job)
        job_sequence.add_job(job_2)
        project.add_or_update_job_sequence(job_sequence)

        job.save_to_db(job_db)
        job_2.save_to_db(job_db)
        project.save_to_db(project_db)

        update_job_sequence(job, job_db, project_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)
        update_job_2 = DBObject.load_from_db(Job, job_2.get_id(), job_db)

        self.assertEqual(
            updated_project.get_active_jobs(), [
                job_2.get_id()])
        self.assertTrue(update_job_2.is_in_progress())
        self.assertEqual(job.get_end_model(), update_job_2.get_start_model())
        self.assertTrue(updated_project.contains_job(job.get_id()))
        self.assertTrue(updated_project.contains_job(job_2.get_id()))
        self.assertEqual(updated_project.get_job_sequence("123dafasdf34sdfsdf").current_model, update_job_2.get_start_model())
        self.assertFalse(update_job_2.should_terminate())

    def test_termination_check_pass(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        builder = JobSequenceBuilder()
        builder.id = "123dafasdf34sdfsdf"
        job_sequence = builder.build()
        job_sequence.current_model = Model(
            "12312414",
            "12312414/start_model",
            "123211")

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
        job_builder.set_job_sequence_id("123dafasdf34sdfsdf")
        config = JobConfiguration(1, 0, "RANDOM", [])
        config.add_termination_criteria(
            DurationTerminationCriteria(
                0, get_epoch_time()))
        job_builder.set_configuration(config.to_json())
        job_builder.set_start_model(
            Model(
                "12312414",
                "12312414/start_model",
                "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()

        job_builder_2 = JobBuilder()
        job_builder_2.set_id("job_test_id_2")
        job_builder_2.set_project_id("test_id")
        job_builder_2.set_job_sequence_id("123dafasdf34sdfsdf")
        job_builder_2.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder_2.set_devices(["34553"])
        job_2 = job_builder_2.build()

        job_sequence.add_job(job)
        job_sequence.add_job(job_2)
        project.add_or_update_job_sequence(job_sequence)

        job.save_to_db(job_db)
        job_2.save_to_db(job_db)
        project.save_to_db(project_db)

        termination_check(job, job_db, project_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)
        update_job_2 = DBObject.load_from_db(Job, job_2.get_id(), job_db)

        self.assertEqual(
            updated_project.get_active_jobs(), [
                job_2.get_id()])
        self.assertTrue(update_job_2.is_in_progress())
        self.assertEqual(job.get_end_model(), update_job_2.get_start_model())
        self.assertTrue(updated_project.contains_job(job.get_id()))
        self.assertTrue(updated_project.contains_job(job_2.get_id()))
        self.assertTrue(job.is_cancelled())
        self.assertEqual(updated_project.get_job_sequence(job_sequence.id).current_model, update_job_2.get_start_model())

    def test_termination_check_pass_2(self):
        project_db = InMemoryDBInterface()
        job_db = InMemoryDBInterface()

        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        builder.set_devices(
            {"34553": {"ID": "34553", "registered_on": "213123144.2342"}})
        project = builder.build()
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        builder = JobSequenceBuilder()
        builder.id = "123dafasdf34sdfsdf"
        job_sequence = builder.build()
        job_sequence.current_model = Model(
            "12312414",
            "12312414/start_model",
            "123211")

        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_project_id("test_id")
        job_builder.set_job_sequence_id("123dafasdf34sdfsdf")
        config = JobConfiguration(1, 0, "RANDOM", [])
        config.add_termination_criteria(
            DurationTerminationCriteria(
                10, get_epoch_time()))
        job_builder.set_configuration(config.to_json())
        job_builder.set_start_model(
            Model(
                "12312414",
                "12312414/start_model",
                "123211").to_json())
        job_builder.set_devices(["34553"])
        job = job_builder.build()

        job_builder_2 = JobBuilder()
        job_builder_2.set_id("job_test_id_2")
        job_builder_2.set_project_id("test_id")
        job_builder_2.set_job_sequence_id("123dafasdf34sdfsdf")
        job_builder_2.set_configuration(
            JobConfiguration(
                1, 0, "RANDOM", []).to_json())
        job_builder_2.set_devices(["34553"])
        job_2 = job_builder_2.build()

        job_sequence.add_job(job)
        job_sequence.add_job(job_2)
        project.add_or_update_job_sequence(job_sequence)

        job.save_to_db(job_db)
        job_2.save_to_db(job_db)
        project.save_to_db(project_db)

        termination_check(job, job_db, project_db)

        updated_project = DBObject.load_from_db(
            Project, project.get_id(), project_db)
        update_job_2 = DBObject.load_from_db(Job, job_2.get_id(), job_db)

        self.assertEqual(updated_project.get_active_jobs(), [job.get_id()])
        self.assertFalse(update_job_2.is_in_progress())
        self.assertTrue(updated_project.contains_job(job.get_id()))
        self.assertTrue(updated_project.contains_job(job_2.get_id()))
        self.assertTrue(job.is_in_progress())
