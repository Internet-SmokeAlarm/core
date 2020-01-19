import unittest

from dependencies.python.fmlaas.model import ApiKeyBuilder

class ApiKeyBuilderTestCase(unittest.TestCase):

    def test_build_pass(self):
        builder = ApiKeyBuilder()
        api_key = builder.build()

    def test_validate_parameters_pass(self):
        builder = ApiKeyBuilder()

        self.assertTrue(builder._validate_paramaters())
