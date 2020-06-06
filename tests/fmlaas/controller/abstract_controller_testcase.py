import unittest

from dependencies.python.fmlaas.model import JobConfiguration
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobSequenceBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum


class AbstractControllerTestCase(unittest.TestCase):

    def _build_simple_project(self):
        project_builder = ProjectBuilder()
        project_builder.set_id("test_id")
        project_builder.set_name("test_name")

        project = project_builder.build()
        project.add_device("12344")
        project.add_or_update_member(
            "user_12345", ProjectPrivilegeTypesEnum.ADMIN)

        return project

    def _build_simple_job_sequence(self):
        builder = JobSequenceBuilder()
        builder.id = "test_id_2"

        return builder.build()

    def _build_simple_job(self):
        job_builder = JobBuilder()
        job_builder.set_id("job_test_id")
        job_builder.set_parent_project_id("test_id")
        job_builder.set_parent_job_sequence_id("test_id_2")
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
                "1234",
                "1234/aggregate_model",
                "123211").to_json())
        job_builder.set_devices(["34553"])

        return job_builder.build()
