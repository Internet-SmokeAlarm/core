import unittest

from dependencies.python.fmlaas.auth import get_resource_list
from dependencies.python.fmlaas.auth import get_resource_method
from dependencies.python.fmlaas.auth import get_user_resource_list
from dependencies.python.fmlaas.auth import get_group_admin_resource_list
from dependencies.python.fmlaas.auth import get_group_member_resource_list
from dependencies.python.fmlaas.auth import get_group_device_resource_list
from dependencies.python.fmlaas.auth import get_group_read_only_member_resource_list
from dependencies.python.fmlaas.auth import get_default_resource_list
from dependencies.python.fmlaas.auth import PermissionsGroupTypeEnum

class GetResourceListTestCase(unittest.TestCase):

    def test_get_group_admin_resource_list_pass(self):
        resources = [
            "v1/round/get/1234/*",
            "v1/round/get/aggregate_model/1234/*",
            "v1/round/get/start_model/1234/*",
            "v1/round/start",

            "v1/group/get/1234",
            "v1/group/get/current_round_id/1234",
            "v1/group/get/initial_model/1234",
            "v1/group/post/initial_model",

            "v1/device/get/active/*",
            "v1/device/register"
        ]
        self.assertEqual(resources, get_group_admin_resource_list("1234", "*", "3453453"))

    def test_get_group_member_resource_list_pass(self):
        resources = [
            "v1/round/get/1234/*",
            "v1/round/get/aggregate_model/1234/*",
            "v1/round/get/start_model/1234/*",
            "v1/round/start",

            "v1/group/get/1234",
            "v1/group/get/current_round_id/1234",
            "v1/group/get/initial_model/1234",
            "v1/group/post/initial_model",

            "v1/device/get/active/*",
            "v1/device/register"
        ]
        self.assertEqual(resources, get_group_member_resource_list("1234", "*", "3453453"))

    def test_get_group_read_only_member_resource_list_pass(self):
        resources = [
            "v1/round/get/1234/*",
            "v1/round/get/aggregate_model/1234/*",
            "v1/round/get/start_model/1234/*",

            "v1/group/get/1234",
            "v1/group/get/current_round_id/1234",
            "v1/group/get/initial_model/1234",

            "v1/device/get/active/*"
        ]
        self.assertEqual(resources, get_group_read_only_member_resource_list("1234", "*", "3453453"))

    def test_get_group_device_resource_list_pass(self):
        resources = [
            "v1/round/get/1234/*",
            "v1/round/get/start_model/1234/*",

            "v1/device/get/active/3453453",
            "v1/submit_model_update",

            "v1/group/get/current_round_id/1234"
        ]
        self.assertEqual(resources, get_group_device_resource_list("1234", "*", "3453453"))

    def test_get_default_resource_list_pass(self):
        self.assertEqual([], get_default_resource_list(None, None, None))

    def test_get_user_resource_list_pass(self):
        resources = [
            "v1/group/create",
            "v1/group/delete"
        ]
        self.assertEqual(resources, get_user_resource_list("1234", "*", "3453453"))

    def test_get_resource_method_pass(self):
        self.assertEqual(get_group_admin_resource_list, get_resource_method(PermissionsGroupTypeEnum.GROUP_ADMIN))
        self.assertEqual(get_group_member_resource_list, get_resource_method(PermissionsGroupTypeEnum.GROUP_MEMBER))
        self.assertEqual(get_group_read_only_member_resource_list, get_resource_method(PermissionsGroupTypeEnum.GROUP_READ_ONLY_MEMBER))
        self.assertEqual(get_group_device_resource_list, get_resource_method(PermissionsGroupTypeEnum.GROUP_DEVICE))
        self.assertEqual(get_user_resource_list, get_resource_method(PermissionsGroupTypeEnum.USER))
        self.assertEqual(get_default_resource_list, get_resource_method(PermissionsGroupTypeEnum.UNAUTHENTICATED))
