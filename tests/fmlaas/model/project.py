import unittest

from dependencies.python.fmlaas.model import Project
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import ProjectPrivilegeTypesEnum
from dependencies.python.fmlaas import generate_unique_id
from dependencies.python.fmlaas import HierarchicalModelNameStructure
from dependencies.python.fmlaas.model import ProjectBuilder


class ProjectTestCase(unittest.TestCase):

    def build_default_project(self):
        builder = ProjectBuilder()
        builder.set_id("id")
        builder.set_name("my_name")

        return builder.build()

    def test_add_device_pass(self):
        project = self.build_default_project()

        device_id, device_api_key = "12311213", "1244535231412"

        project.add_device(device_id)

        self.assertTrue(device_id in project.get_devices())

    def test_to_json_pass(self):
        project = self.build_default_project()

        device_id, device_api_key = "12311213", "1244535231412"

        project.add_device(device_id)

        json_data = project.to_json()

        self.assertTrue("ID" in json_data)
        self.assertTrue("devices" in json_data)
        self.assertEqual(len(json_data["devices"]), 1)
        self.assertTrue("job_info" in json_data)
        self.assertTrue("job_paths" in json_data)
        self.assertTrue("current_job_ids" in json_data)
        self.assertTrue("members" in json_data)
        self.assertTrue("billing" in json_data)

    def test_to_json_pass_2(self):
        project = self.build_default_project()

        device_id, device_api_key = "12311213", "1244535231412"
        project.add_device(device_id)

        device_id_2, device_api_key_2 = "54634324535", "324o823uo2ou3o234"
        project.add_device(device_id_2)

        json_data = project.to_json()

        self.assertTrue("ID" in json_data)
        self.assertTrue("devices" in json_data)
        self.assertEqual(len(json_data["devices"]), 2)
        self.assertTrue("job_info" in json_data)
        self.assertTrue("job_paths" in json_data)
        self.assertTrue("current_job_ids" in json_data)
        self.assertTrue("members" in json_data)
        self.assertTrue("billing" in json_data)

    def test_from_json_pass(self):
        json_data = {
            'name': 'a_different_name',
            'current_job_ids': [],
            'ID': 'id',
            'devices': {
                '6617961791227642': {
                    'ID': '6617961791227642',
                    'registered_on': "1576779269.11093"},
                '6336011475872533': {
                    'ID': '6336011475872533',
                    'registered_on': "1576779269.110966"}},
            'job_info': {},
            "job_paths": [],
            "members": {},
            "billing": {}}

        project = Project.from_json(json_data)

        self.assertEqual(project.get_name(), "a_different_name")
        self.assertEqual(project.get_id(), "id")
        self.assertEqual(project.get_current_job_ids(), [])
        self.assertEqual(
            project.get_devices(), {
                '6617961791227642': {
                    'ID': '6617961791227642', 'registered_on': "1576779269.11093"}, '6336011475872533': {
                    'ID': '6336011475872533', 'registered_on': "1576779269.110966"}})
        self.assertEqual(project.members, {})
        self.assertEqual(project.get_job_paths(), [])
        self.assertEqual(project.get_job_info(), {})
        self.assertEqual(project.get_billing(), {})

    def test_from_json_pass_2(self):
        project = self.build_default_project()
        project.add_device("7897956979947357")
        project.add_device("1822867963788927")

        project.add_or_update_member(
            "user_1234456", ProjectPrivilegeTypesEnum.OWNER)
        project.add_or_update_member(
            "user_123445", ProjectPrivilegeTypesEnum.ADMIN)
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.READ_ONLY)

        project.create_job_path("34345234123")
        project.add_job_to_path_prev_id("34345234123", "564324234")
        project.add_job_to_path_prev_id("564324234", "6324213123")
        project.create_job_path("12312445123")

        project.add_current_job_id("34345234123")
        project.add_current_job_id("12312445123")

        json_project = Project.from_json(project.to_json())

        self.assertEqual(project.get_name(), json_project.get_name())
        self.assertEqual(project.get_id(), json_project.get_id())
        self.assertEqual(project.get_job_info(), json_project.get_job_info())
        self.assertEqual(project.get_devices(), json_project.get_devices())
        self.assertEqual(
            project.get_current_job_ids(),
            json_project.get_current_job_ids())
        self.assertEqual(project.get_members(), json_project.get_members())

    def test_contains_job_pass(self):
        project = self.build_default_project()

        project.create_job_path("12324512")

        self.assertTrue(project.contains_job("12324512"))

    def test_contains_job_fail(self):
        project = self.build_default_project()

        project.create_job_path("1234414")
        job_id_2 = "i_dont_exist"

        self.assertFalse(project.contains_job(job_id_2))

    def test_get_device_list_pass(self):
        project = self.build_default_project()

        self.assertEqual(0, len(project.get_device_list()))

        device_id, device_api_key = "12311213", "1244535231412"
        project.add_device(device_id)
        device_id_2, device_api_key_2 = "6768564345", "343454efafsdffsdfsfsdfs"
        project.add_device(device_id_2)

        self.assertEqual(2, len(project.get_device_list()))
        self.assertTrue(device_id in project.get_device_list())
        self.assertTrue(device_id_2 in project.get_device_list())

    def test_add_current_job_id_pass(self):
        project = self.build_default_project()

        project.add_current_job_id("4142634852358226")

        self.assertTrue("4142634852358226" in project.get_current_job_ids())

    def test_remove_current_job_id_pass(self):
        project = self.build_default_project()

        project.add_current_job_id("4142634852358226")
        project.add_current_job_id("6768564345")
        project.remove_current_job_id("4142634852358226")

        self.assertFalse("4142634852358226" in project.get_current_job_ids())
        self.assertTrue("6768564345" in project.get_current_job_ids())

    def test_add_job_info_pass(self):
        project = self.build_default_project()

        self.assertFalse("665544343443" in project.get_job_info())

        project._add_job_info("665544343443")

        self.assertTrue("665544343443" in project.get_job_info())

    def test_create_job_path_pass(self):
        project = self.build_default_project()

        self.assertEqual(0, len(project.get_job_paths()))

        project.create_job_path("34345234123")

        self.assertEqual(1, len(project.get_job_paths()))
        self.assertEqual(["34345234123"], project.get_job_paths()[0])
        self.assertTrue("34345234123" in project.get_job_info())

    def test_create_job_path_fail(self):
        project = self.build_default_project()

        project.create_job_path("34345234123")
        project.add_job_to_path_prev_id("34345234123", "564324234")
        project.create_job_path("34345234123")

        self.assertEqual(["34345234123", "564324234"],
                         project.get_job_paths()[0])

    def test_add_job_to_path_prev_id_pass(self):
        project = self.build_default_project()

        project.create_job_path("34345234123")
        project.add_job_to_path_prev_id("34345234123", "564324234")
        project.add_job_to_path_prev_id("564324234", "6324213123")
        project.create_job_path("12312445123")

        self.assertEqual(["34345234123", "564324234",
                          "6324213123"], project.get_job_paths()[0])
        self.assertEqual(["12312445123"], project.get_job_paths()[1])
        self.assertTrue("34345234123" in project.get_job_info())
        self.assertTrue("564324234" in project.get_job_info())
        self.assertTrue("6324213123" in project.get_job_info())
        self.assertTrue("12312445123" in project.get_job_info())

    def test_add_job_to_path_prev_id_fail(self):
        project = self.build_default_project()

        project.create_job_path("34345234123")
        project.add_job_to_path_prev_id("34345234123", "564324234")
        project.add_job_to_path_prev_id("6324213123", "63242131235")

        self.assertEqual(["34345234123", "564324234"],
                         project.get_job_paths()[0])
        self.assertTrue("34345234123" in project.get_job_info())
        self.assertTrue("564324234" in project.get_job_info())
        self.assertFalse("63242131235" in project.get_job_info())

    def test_is_member_pass(self):
        project = self.build_default_project()
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.ADMIN)

        self.assertTrue(project.is_member("user_12344"))
        self.assertFalse(project.is_member("user_12345"))

    def test_add_or_update_member_pass(self):
        project = self.build_default_project()

        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.ADMIN)

        self.assertTrue("user_12344" in project.members)

    def test_does_member_have_auth_pass(self):
        project = self.build_default_project()
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
        project = self.build_default_project()
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
        project = self.build_default_project()
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
        project = self.build_default_project()
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.READ_ONLY)

        self.assertEqual(
            ProjectPrivilegeTypesEnum.READ_ONLY,
            project.get_member_auth_level("user_12344"))

    def test_contains_device_pass(self):
        project = self.build_default_project()

        self.assertFalse(project.contains_device("userser123123"))

        project.add_device("sfksdsf")

        self.assertTrue(project.contains_device("sfksdsf"))
        self.assertFalse(project.contains_device("123123141"))

    def test_get_next_job_in_sequence_pass(self):
        project = self.build_default_project()

        project.create_job_path("123343412")
        project.add_job_to_path_prev_id("123343412", "23423234")
        project.create_job_path("345234242")
        project.add_job_to_path_prev_id("23423234", "6345234242")
        project.create_job_path("84839222")

        self.assertEqual(
            "6345234242",
            project.get_next_job_in_sequence("23423234"))
        self.assertEqual(None, project.get_next_job_in_sequence("84839222"))
        self.assertEqual(None, project.get_next_job_in_sequence("6345234242"))
