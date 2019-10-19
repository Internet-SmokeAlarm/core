import unittest
from ..utils import generate_group_key

class GroupKeyGenerationTestCase(unittest.TestCase):

    def test_generate_group_key(self):
        group_key = generate_group_key("test_group_name_1234")

        self.assertTrue("test_group_name_1234" in group_key)
