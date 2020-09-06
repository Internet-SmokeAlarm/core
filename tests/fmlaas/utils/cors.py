import unittest

from dependencies.python.fmlaas.utils import get_allowed_origins

class CorsTestCase(unittest.TestCase):

    def test_get_allowed_origins(self):
        self.assertEqual(get_allowed_origins(), "*")
