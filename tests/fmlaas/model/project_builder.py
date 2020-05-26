from dependencies.python.fmlaas.model import ProjectBuilder
from .abstract_model_testcase import AbstractModelTestCase


class ProjectBuilderTestCase(AbstractModelTestCase):

    def test_build_pass(self):
        project = self._build_simple_project(1)

        self.assertEqual(project.to_json(), self._get_simple_project_json(1))

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
