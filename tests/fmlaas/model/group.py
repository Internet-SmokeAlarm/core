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
        self.assertTrue("rounds" in json_data)

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
        self.assertTrue("rounds" in json_data)

    def test_from_json_pass(self):
        json_data = {'name': 'a_different_name', 'current_round_id' : "N/A", 'ID': 'id', 'devices': {'6617961791227642': {'ID': '6617961791227642', 'registered_on': "1576779269.11093"}, '6336011475872533': {'ID': '6336011475872533', 'registered_on': "1576779269.110966"}}, 'rounds': {}, "members" : {}}

        group = FLGroup.from_json(json_data)

        self.assertEqual(group.get_name(), "a_different_name")
        self.assertEqual(group.get_id(), "id")
        self.assertEqual(group.get_rounds(), {})
        self.assertEqual(group.get_devices(), {'6617961791227642': {'ID': '6617961791227642', 'registered_on': "1576779269.11093"}, '6336011475872533': {'ID': '6336011475872533', 'registered_on': "1576779269.110966"}})
        self.assertEqual(group.members, {})

    def test_from_json_pass_2(self):
        json_data = {'current_round_id' : "N/A", 'name': 'a_different_name', 'ID': 'id10', 'devices': {'7897956979947357': {'ID': '7897956979947357', 'registered_on': "1576779498.189228"}, '1822867963788927': {'ID': '1822867963788927', 'registered_on': "1576779498.189258"}}, 'rounds': {'4152602852358113': {'ID': '4152602852358113', 'status': 'IN_PROGRESS', 'devices': ['7897956979947357', '1822867963788927'], 'previous_round_id': 'N/A', 'aggregate_model': 'N/A', 'configuration': {'num_devices': "0"}, 'models': {}, 'created_on': "1576779498.189267"}}, "members" : {}}

        group = FLGroup.from_json(json_data)

        self.assertEqual(group.get_name(), "a_different_name")
        self.assertEqual(group.get_id(), "id10")
        self.assertEqual(group.get_rounds(), {'4152602852358113': {'ID': '4152602852358113', 'status': 'IN_PROGRESS', 'devices': ['7897956979947357', '1822867963788927'], 'previous_round_id': 'N/A', 'aggregate_model': 'N/A', 'configuration': {'num_devices': "0"}, 'models': {}, 'created_on': "1576779498.189267"}})
        self.assertEqual(group.get_devices(), {'7897956979947357': {'ID': '7897956979947357', 'registered_on': "1576779498.189228"}, '1822867963788927': {'ID': '1822867963788927', 'registered_on': "1576779498.189258"}})
        self.assertEqual(group.get_current_round_id(), "N/A")
        self.assertEqual(group.members, {})

    def test_add_round_pass(self):
        group = self.build_default_group()

        round_id = generate_unique_id()
        builder = RoundBuilder()
        builder.set_id(round_id)
        builder.set_configuration(RoundConfiguration("0", "RANDOM").to_json())
        builder.set_start_model(Model("1234", "1234/1234", "1234554").to_json())
        round = builder.build()

        group.add_round(round.get_id())

        self.assertTrue(group.contains_round(round.get_id()))

    def test_contains_round_pass(self):
        group = self.build_default_group()

        group.add_round("12324512")

        self.assertTrue(group.contains_round("12324512"))

    def test_contains_round_fail(self):
        group = self.build_default_group()

        group.add_round("1234414")
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

    def test_set_current_round_pass(self):
        json_data = {'current_round_id' : "4152602852358113", 'name': 'a_different_name', 'ID': 'id10', 'devices': {'7897956979947357': {'ID': '7897956979947357', 'registered_on': "1576779498"}, '1822867963788927': {'ID': '1822867963788927', 'registered_on': "1576779498"}}, 'rounds': {'4152602852358113': {'ID': '4152602852358113', 'status': 'IN_PROGRESS', 'devices': ['7897956979947357', '1822867963788927'], 'previous_round_id': 'N/A', 'aggregate_model': 'N/A', 'configuration': {'num_devices': "0"}, 'models': {}, 'created_on': "1576779498"}, '4142634852358226': {'ID': '4142634852358226', 'status': 'CANCELLED', 'devices': ['7897956979947357', '1822867963788927'], 'previous_round_id': 'N/A', 'aggregate_model': 'N/A', 'configuration': {'num_devices': "0"}, 'models': {}, 'created_on': "1576779498"}}, "members" : {}}

        group = FLGroup.from_json(json_data)

        group.set_current_round_id("4142634852358226")

        self.assertEqual(group.current_round_id, "4142634852358226")

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
