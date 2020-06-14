from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas import generate_unique_id
from dependencies.python.fmlaas import HierarchicalModelNameStructure
from dependencies.python.fmlaas.model import ProjectBuilder
from dependencies.python.fmlaas.model import JobSequence
from dependencies.python.fmlaas.model import JobSequenceBuilder
from dependencies.python.fmlaas.model import JobBuilder
from dependencies.python.fmlaas.model import JobConfiguration
from .abstract_model_testcase import AbstractModelTestCase


class ProjectTestCase(AbstractModelTestCase):

    def test_add_device_pass(self):
        project = self._build_simple_project(1)

        device_id, device_api_key = "12311213", "1244535231412"

        project.add_device(device_id)

        self.assertTrue(device_id in project.get_devices())

    def test_to_json_simple_pass(self):
        project = self._build_simple_project(1)
        simple_project_json = self._get_simple_project_json(1)

        self.assertEqual(project.to_json(), simple_project_json)

    def test_from_json_simple_pass(self):
        json_data = self._get_simple_project_json(1)
        project = Project.from_json(json_data)

        self.assertEqual(project, self._build_simple_project(1))

    def test_to_json_complex_pass(self):
        project = self._build_simple_project(1)

        device_id, device_api_key = "12311213", "1244535231412"
        project.add_device(device_id)

        device_id_2, device_api_key_2 = "54634324535", "324o823uo2ou3o234"
        project.add_device(device_id_2)

        json_data = project.to_json()

        self.assertTrue("ID" in json_data)
        self.assertTrue("devices" in json_data)
        self.assertEqual(len(json_data["devices"]), 2)
        self.assertTrue("job_sequences" in json_data)
        self.assertTrue("members" in json_data)
        self.assertTrue("billing" in json_data)

    def test_to_from_json_complex_pass(self):
        project = self._build_simple_project(1)
        project.add_device("7897956979947357")
        project.add_device("1822867963788927")

        project.add_or_update_member(
            "user_1234456", ProjectPrivilegeTypesEnum.OWNER)
        project.add_or_update_member(
            "user_123445", ProjectPrivilegeTypesEnum.ADMIN)
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.READ_ONLY)

        job_sequence, _ = self._build_default_job_sequence()
        job_sequence.id = "34345234123"
        job_sequence.add_job(self._build_job(1))
        job_sequence.add_job(self._build_job(2))

        job_sequence_2, _ = self._build_default_job_sequence()
        job_sequence_2.id = "12312445123"
        job_sequence_2.add_job(self._build_job(3))

        project.add_or_update_job_sequence(job_sequence)
        project.add_or_update_job_sequence(job_sequence_2)

        json_project = Project.from_json(project.to_json())

        self.assertEqual(project, json_project)

    def test_get_device_list_pass(self):
        project = self._build_simple_project(1)

        self.assertEqual(0, len(project.get_device_list()))

        device_id, device_api_key = "12311213", "1244535231412"
        project.add_device(device_id)
        device_id_2, device_api_key_2 = "6768564345", "343454efafsdffsdfsfsdfs"
        project.add_device(device_id_2)

        self.assertEqual(2, len(project.get_device_list()))
        self.assertTrue(device_id in project.get_device_list())
        self.assertTrue(device_id_2 in project.get_device_list())

    def test_is_member_pass(self):
        project = self._build_simple_project(1)
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.ADMIN)

        self.assertTrue(project.is_member("user_12344"))
        self.assertFalse(project.is_member("user_12345"))

    def test_add_or_update_member_pass(self):
        project = self._build_simple_project(1)

        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.ADMIN)

        self.assertTrue("user_12344" in project.members)

    def test_does_member_have_auth_pass(self):
        project = self._build_simple_project(1)
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.ADMIN)

        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.ADMIN))
        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_WRITE))
        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_ONLY))

    def test_does_member_have_auth_pass_2(self):
        project = self._build_simple_project(1)
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.READ_WRITE)

        self.assertFalse(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.ADMIN))
        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_WRITE))
        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_ONLY))

    def test_does_member_have_auth_pass_3(self):
        project = self._build_simple_project(1)
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.READ_ONLY)

        self.assertFalse(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.ADMIN))
        self.assertFalse(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_WRITE))
        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_ONLY))

    def test_get_member_auth_level_pass(self):
        project = self._build_simple_project(1)
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.READ_ONLY)

        self.assertEqual(
            ProjectPrivilegeTypesEnum.READ_ONLY,
            project.get_member_auth_level("user_12344"))

    def test_contains_device_pass(self):
        project = self._build_simple_project(1)

        self.assertFalse(project.contains_device("userser123123"))

        project.add_device("sfksdsf")

        self.assertTrue(project.contains_device("sfksdsf"))
        self.assertFalse(project.contains_device("123123141"))

    def test_equals_simple_pass(self):
        project_1 = self._build_simple_project(1)
        project_2 = self._build_simple_project(2)
        project_3 = self._build_simple_project(1)

        self.assertEqual(project_1, project_3)
        self.assertNotEqual(project_1, project_2)
        self.assertNotEqual(project_2, project_3)

    def test_equals_hard_pass(self):
        project_1 = self._build_simple_project(1)
        project_3 = self._build_simple_project(1)

        project_1.add_or_update_member(
            "user_1234456", ProjectPrivilegeTypesEnum.OWNER)

        self.assertNotEqual(project_1, project_3)

    def test_add_or_update_job_sequence_pass(self):
        project = self._build_simple_project(1)

        job_sequence, json_data = self._build_default_job_sequence()
        project.add_or_update_job_sequence(job_sequence)

        self.assertEqual(json_data, project.job_sequences[job_sequence.id])

    def test_get_job_sequence_pass(self):
        project = self._build_simple_project(1)

        job_sequence, json_data = self._build_default_job_sequence()
        project.add_or_update_job_sequence(job_sequence)

        self.assertEqual(job_sequence, project.get_job_sequence(job_sequence.id))

    def test_contains_job_pass(self):
        project = self._build_simple_project(1)

        job_sequence, _ = self._build_default_job_sequence()
        job_sequence_2, _ = self._build_default_job_sequence()
        job_sequence_2.id = "123123123"

        job_1 = self._build_job(1)
        job_2 = self._build_job(2)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)

        job_sequence.add_job(job_1)
        job_sequence.add_job(job_3)
        job_sequence_2.add_job(job_4)

        project.add_or_update_job_sequence(job_sequence)
        project.add_or_update_job_sequence(job_sequence_2)

        self.assertTrue(project.contains_job(job_1.get_id()))
        self.assertFalse(project.contains_job(job_2.get_id()))
        self.assertTrue(project.contains_job(job_3.get_id()))
        self.assertTrue(project.contains_job(job_4.get_id()))

    def test_get_active_jobs_pass(self):
        project = self._build_simple_project(1)

        job_sequence, _ = self._build_default_job_sequence()
        job_sequence_2, _ = self._build_default_job_sequence()
        job_sequence_2.id = "123123123"

        job_1 = self._build_job(1)
        job_3 = self._build_job(3)
        job_4 = self._build_job(4)

        job_sequence.add_job(job_1)
        job_sequence.add_job(job_3)
        job_sequence_2.add_job(job_4)

        project.add_or_update_job_sequence(job_sequence)
        project.add_or_update_job_sequence(job_sequence_2)

        self.assertTrue(job_1.get_id() in project.get_active_jobs())
        self.assertTrue(job_4.get_id() in project.get_active_jobs())
        self.assertFalse(job_3.get_id() in project.get_active_jobs())

    def test_get_job_sequences_pass(self):
        project = self._build_simple_project(1)

        project.add_or_update_job_sequence(self._build_parameterized_job_sequence(1))
        project.add_or_update_job_sequence(self._build_parameterized_job_sequence(2))
        project.add_or_update_job_sequence(self._build_parameterized_job_sequence(3))
        project.add_or_update_job_sequence(self._build_parameterized_job_sequence(4))
        project.add_or_update_job_sequence(self._build_parameterized_job_sequence(5))

        job_sequences = project.get_job_sequences()

        self.assertEqual(len(job_sequences), 5)
        self.assertEqual(type(job_sequences[0]), JobSequence)
        self.assertEqual(type(job_sequences[1]), JobSequence)
        self.assertEqual(type(job_sequences[2]), JobSequence)
        self.assertEqual(type(job_sequences[3]), JobSequence)
        self.assertEqual(type(job_sequences[4]), JobSequence)

    def test_get_all_jobs_ids_pass(self):
        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        project = builder.build()

        for i in range(10):
            builder = JobSequenceBuilder()
            id = "123dafasdf34sdfsdf_{}".format(i)
            builder.id = id
            job_sequence = builder.build()

            for j in range(5):
                job_builder = JobBuilder()
                job_builder.set_id("job_test_id_{}_{}".format(i, j))
                job_builder.set_project_id("test_id")
                job_builder.set_job_sequence_id(id)
                config = JobConfiguration(1, 0, "RANDOM", [])
                job_builder.set_configuration(config.to_json())
                job_builder.set_devices(["34553"])
                job = job_builder.build()

                job_sequence.add_job(job)

            project.add_or_update_job_sequence(job_sequence)

        project_job_ids = project.get_all_job_ids()

        self.assertEqual(len(project_job_ids), 50)

    def test_contains_job_sequence_pass(self):
        builder = ProjectBuilder()
        builder.set_id("test_id")
        builder.set_name("test_name")
        project = builder.build()

        for i in range(10):
            builder = JobSequenceBuilder()
            id = "123dafasdf34sdfsdf_{}".format(i)
            builder.id = id
            job_sequence = builder.build()

            project.add_or_update_job_sequence(job_sequence)

        self.assertTrue(project.contains_job_sequence("123dafasdf34sdfsdf_5"))
        self.assertFalse(project.contains_job_sequence("123dafasdf34sdfsdf_50"))
