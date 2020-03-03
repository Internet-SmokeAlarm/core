import unittest

from dependencies.python.fmlaas.model import FLGroup
from dependencies.python.fmlaas.model import Round
from dependencies.python.fmlaas.model import RoundBuilder
from dependencies.python.fmlaas.model import Model
from dependencies.python.fmlaas.model import RoundStatus
from dependencies.python.fmlaas.model import RoundConfiguration
from dependencies.python.fmlaas.model import GroupPrivilegeTypesEnum
from dependencies.python.fmlaas import generate_unique_id
from dependencies.python.fmlaas import HierarchicalModelNameStructure
from dependencies.python.fmlaas.model import GroupBuilder
from dependencies.python.fmlaas.device_selection import RandomDeviceSelector

class FLGroupTestCase(unittest.TestCase):

    def build_default_group(self):
        builder = GroupBuilder()
        builder.set_id("id")
        builder.set_name("my_name")

        return builder.build()

    def test_add_device_pass(self):
        group = self.build_default_group()

        device_id, device_api_key = "12311213", "1244535231412"

        group.add_device(device_id)

        self.assertTrue(device_id in group.get_devices())

    def test_to_json_pass(self):
        group = self.build_default_group()

        device_id, device_api_key = "12311213", "1244535231412"

        group.add_device(device_id)

        json_data = group.to_json()

        self.assertTrue("ID" in json_data)
        self.assertTrue("devices" in json_data)
        self.assertEqual(len(json_data["devices"]), 1)
        self.assertTrue("round_info" in json_data)
        self.assertTrue("round_paths" in json_data)
        self.assertTrue("current_round_ids" in json_data)
        self.assertTrue("members" in json_data)
        self.assertTrue("billing" in json_data)

    def test_to_json_pass_2(self):
        group = self.build_default_group()

        device_id, device_api_key = "12311213", "1244535231412"
        group.add_device(device_id)

        device_id_2, device_api_key_2 = "54634324535", "324o823uo2ou3o234"
        group.add_device(device_id_2)

        json_data = group.to_json()

        self.assertTrue("ID" in json_data)
        self.assertTrue("devices" in json_data)
        self.assertEqual(len(json_data["devices"]), 2)
        self.assertTrue("round_info" in json_data)
        self.assertTrue("round_paths" in json_data)
        self.assertTrue("current_round_ids" in json_data)
        self.assertTrue("members" in json_data)
        self.assertTrue("billing" in json_data)

    def test_from_json_pass(self):
        json_data = {'name': 'a_different_name', 'current_round_ids' : [], 'ID': 'id', 'devices': {'6617961791227642': {'ID': '6617961791227642', 'registered_on': "1576779269.11093"}, '6336011475872533': {'ID': '6336011475872533', 'registered_on': "1576779269.110966"}}, 'round_info': {}, "round_paths" : [], "members" : {}, "billing" : {}}

        group = FLGroup.from_json(json_data)

        self.assertEqual(group.get_name(), "a_different_name")
        self.assertEqual(group.get_id(), "id")
        self.assertEqual(group.get_current_round_ids(), [])
        self.assertEqual(group.get_devices(), {'6617961791227642': {'ID': '6617961791227642', 'registered_on': "1576779269.11093"}, '6336011475872533': {'ID': '6336011475872533', 'registered_on': "1576779269.110966"}})
        self.assertEqual(group.members, {})
        self.assertEqual(group.get_round_paths(), [])
        self.assertEqual(group.get_round_info(), {})
        self.assertEqual(group.get_billing(), {})

    def test_from_json_pass_2(self):
        group = self.build_default_group()
        group.add_device("7897956979947357")
        group.add_device("1822867963788927")

        group.add_or_update_member("user_1234456", GroupPrivilegeTypesEnum.OWNER)
        group.add_or_update_member("user_123445", GroupPrivilegeTypesEnum.ADMIN)
        group.add_or_update_member("user_12344", GroupPrivilegeTypesEnum.READ_ONLY)

        group.create_round_path("34345234123")
        group.add_round_to_path_prev_id("34345234123", "564324234")
        group.add_round_to_path_prev_id("564324234", "6324213123")
        group.create_round_path("12312445123")

        group.add_current_round_id("34345234123")
        group.add_current_round_id("12312445123")

        json_group = FLGroup.from_json(group.to_json())

        self.assertEqual(group.get_name(), json_group.get_name())
        self.assertEqual(group.get_id(), json_group.get_id())
        self.assertEqual(group.get_round_info(), json_group.get_round_info())
        self.assertEqual(group.get_devices(), json_group.get_devices())
        self.assertEqual(group.get_current_round_ids(), json_group.get_current_round_ids())
        self.assertEqual(group.get_members(), json_group.get_members())

    def test_contains_round_pass(self):
        group = self.build_default_group()

        group.create_round_path("12324512")

        self.assertTrue(group.contains_round("12324512"))

    def test_contains_round_fail(self):
        group = self.build_default_group()

        group.create_round_path("1234414")
        round_id_2 = "i_dont_exist"

        self.assertFalse(group.contains_round(round_id_2))

    def test_get_device_list_pass(self):
        group = self.build_default_group()

        self.assertEqual(0, len(group.get_device_list()))

        device_id, device_api_key = "12311213", "1244535231412"
        group.add_device(device_id)
        device_id_2, device_api_key_2 = "6768564345", "343454efafsdffsdfsfsdfs"
        group.add_device(device_id_2)

        self.assertEqual(2, len(group.get_device_list()))
        self.assertTrue(device_id in group.get_device_list())
        self.assertTrue(device_id_2 in group.get_device_list())

    def test_add_current_round_id_pass(self):
        group = self.build_default_group()

        group.add_current_round_id("4142634852358226")

        self.assertTrue("4142634852358226" in group.get_current_round_ids())

    def test_remove_current_round_id_pass(self):
        group = self.build_default_group()

        group.add_current_round_id("4142634852358226")
        group.add_current_round_id("6768564345")
        group.remove_current_round_id("4142634852358226")

        self.assertFalse("4142634852358226" in group.get_current_round_ids())
        self.assertTrue("6768564345" in group.get_current_round_ids())

    def test_add_round_info_pass(self):
        group = self.build_default_group()

        self.assertFalse("665544343443" in group.get_round_info())

        group._add_round_info("665544343443")

        self.assertTrue("665544343443" in group.get_round_info())

    def test_create_round_path_pass(self):
        group = self.build_default_group()

        self.assertEqual(0, len(group.get_round_paths()))

        group.create_round_path("34345234123")

        self.assertEqual(1, len(group.get_round_paths()))
        self.assertEqual(["34345234123"], group.get_round_paths()[0])
        self.assertTrue("34345234123" in group.get_round_info())

    def test_create_round_path_fail(self):
        group = self.build_default_group()

        group.create_round_path("34345234123")
        group.add_round_to_path_prev_id("34345234123", "564324234")
        group.create_round_path("34345234123")

        self.assertEqual(["34345234123", "564324234"], group.get_round_paths()[0])

    def test_add_round_to_path_prev_id_pass(self):
        group = self.build_default_group()

        group.create_round_path("34345234123")
        group.add_round_to_path_prev_id("34345234123", "564324234")
        group.add_round_to_path_prev_id("564324234", "6324213123")
        group.create_round_path("12312445123")

        self.assertEqual(["34345234123", "564324234", "6324213123"], group.get_round_paths()[0])
        self.assertEqual(["12312445123"], group.get_round_paths()[1])
        self.assertTrue("34345234123" in group.get_round_info())
        self.assertTrue("564324234" in group.get_round_info())
        self.assertTrue("6324213123" in group.get_round_info())
        self.assertTrue("12312445123" in group.get_round_info())

    def test_add_round_to_path_prev_id_fail(self):
        group = self.build_default_group()

        group.create_round_path("34345234123")
        group.add_round_to_path_prev_id("34345234123", "564324234")
        group.add_round_to_path_prev_id("6324213123", "63242131235")

        self.assertEqual(["34345234123", "564324234"], group.get_round_paths()[0])
        self.assertTrue("34345234123" in group.get_round_info())
        self.assertTrue("564324234" in group.get_round_info())
        self.assertFalse("63242131235" in group.get_round_info())

    def test_is_member_pass(self):
        group = self.build_default_group()
        group.add_or_update_member("user_12344", GroupPrivilegeTypesEnum.ADMIN)

        self.assertTrue(group.is_member("user_12344"))
        self.assertFalse(group.is_member("user_12345"))

    def test_add_or_update_member_pass(self):
        group = self.build_default_group()

        group.add_or_update_member("user_12344", GroupPrivilegeTypesEnum.ADMIN)

        self.assertTrue("user_12344" in group.members)

    def test_does_member_have_auth_pass(self):
        group = self.build_default_group()
        group.add_or_update_member("user_12344", GroupPrivilegeTypesEnum.ADMIN)

        self.assertTrue(group.does_member_have_auth("user_12344", GroupPrivilegeTypesEnum.ADMIN))
        self.assertTrue(group.does_member_have_auth("user_12344", GroupPrivilegeTypesEnum.READ_WRITE))
        self.assertTrue(group.does_member_have_auth("user_12344", GroupPrivilegeTypesEnum.READ_ONLY))

    def test_does_member_have_auth_pass_2(self):
        group = self.build_default_group()
        group.add_or_update_member("user_12344", GroupPrivilegeTypesEnum.READ_WRITE)

        self.assertFalse(group.does_member_have_auth("user_12344", GroupPrivilegeTypesEnum.ADMIN))
        self.assertTrue(group.does_member_have_auth("user_12344", GroupPrivilegeTypesEnum.READ_WRITE))
        self.assertTrue(group.does_member_have_auth("user_12344", GroupPrivilegeTypesEnum.READ_ONLY))

    def test_does_member_have_auth_pass_3(self):
        group = self.build_default_group()
        group.add_or_update_member("user_12344", GroupPrivilegeTypesEnum.READ_ONLY)

        self.assertFalse(group.does_member_have_auth("user_12344", GroupPrivilegeTypesEnum.ADMIN))
        self.assertFalse(group.does_member_have_auth("user_12344", GroupPrivilegeTypesEnum.READ_WRITE))
        self.assertTrue(group.does_member_have_auth("user_12344", GroupPrivilegeTypesEnum.READ_ONLY))

    def test_get_member_auth_level_pass(self):
        group = self.build_default_group()
        group.add_or_update_member("user_12344", GroupPrivilegeTypesEnum.READ_ONLY)

        self.assertEqual(GroupPrivilegeTypesEnum.READ_ONLY, group.get_member_auth_level("user_12344"))

    def test_contains_device_pass(self):
        group = self.build_default_group()

        self.assertFalse(group.contains_device("userser123123"))

        group.add_device("sfksdsf")

        self.assertTrue(group.contains_device("sfksdsf"))
        self.assertFalse(group.contains_device("123123141"))

    def test_get_next_round_in_sequence_pass(self):
        group = self.build_default_group()

        group.create_round_path("123343412")
        group.add_round_to_path_prev_id("123343412", "23423234")
        group.create_round_path("345234242")
        group.add_round_to_path_prev_id("23423234", "6345234242")
        group.create_round_path("84839222")

        self.assertEqual("6345234242", group.get_next_round_in_sequence("23423234"))
        self.assertEqual(None, group.get_next_round_in_sequence("84839222"))
        self.assertEqual(None, group.get_next_round_in_sequence("6345234242"))
