import unittest

from dependencies.python.fmlaas.model import ApiKeyBuilder
from dependencies.python.fmlaas.auth import PermissionsGroupTypeEnum

class ApiKeyBuilderTestCase(unittest.TestCase):

    def test_build_pass(self):
        builder = ApiKeyBuilder()
        builder.set_permissions_group(PermissionsGroupTypeEnum.GROUP_ADMIN)
        api_key = builder.build()

    def test_validate_parameters_pass(self):
        builder = ApiKeyBuilder()
        builder.set_permissions_group(PermissionsGroupTypeEnum.GROUP_ADMIN)

        builder._validate_paramaters()

    def test_validate_parameters_fail(self):
        builder = ApiKeyBuilder()

        self.assertRaises(ValueError, builder._validate_paramaters)
