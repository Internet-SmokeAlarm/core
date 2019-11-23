import unittest

from dependencies.python.fmlaas import HierarchicalModelNameStructure

class HierarchicalModelNameStructureTestCase(unittest.TestCase):

    def test_generate_name(self):
        group_id = "1234"
        round_id = "44563"
        device_id = "6665"

        name = HierarchicalModelNameStructure()
        name.generate_name(group_id, round_id, device_id)

        self.assertEqual("1234/44563/6665", name.get_name())

    def test_get_group_id(self):
        name_txt = "1234/5678/9999"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertEqual(name.get_group_id(), 1234)

    def test_get_round_id(self):
        name_txt = "1234/5678/9999"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertEqual(name.get_round_id(), 5678)

    def test_get_device_id(self):
        name_txt = "1234/5678/9999"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertEqual(name.get_device_id(), 9999)
