import unittest

from dependencies.python.fmlaas.model import ProjectBuilder


class ProjectBuilderTestCase(unittest.TestCase):

    def test_build_pass_1(self):
        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        project = builder.build()

        self.assertEqual(project.get_name(), "test_name")
        self.assertEqual(project.get_id(), "test_id")
        self.assertEqual(project.get_devices(), {})
        self.assertEqual(project.get_job_info(), {})
        self.assertEqual(project.get_current_job_ids(), [])
        self.assertEqual(project.get_job_paths(), [])
        self.assertEqual(project.get_billing(), {})

    def test_build_fail_1(self):
        builder = ProjectBuilder()
        builder.set_id("test_id")

        self.assertRaises(ValueError, builder.build)

    def test_build_fail_2(self):
        builder = ProjectBuilder()
        builder.set_name("test_name")

        self.assertRaises(ValueError, builder.build)

    def test_validate_parameters_pass(self):
        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")

        builder._validate_parameters()

    def test_validate_parameters_fail_1(self):
        builder = ProjectBuilder()
        builder.set_id("test_id")

        self.assertRaises(ValueError, builder._validate_parameters)

    def test_validate_parameters_fail_2(self):
        builder = ProjectBuilder()
        builder.set_name("test_name")

        self.assertRaises(ValueError, builder._validate_parameters)
