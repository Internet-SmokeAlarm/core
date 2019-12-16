import unittest

from dependencies.python.fmlaas import HierarchicalModelNameStructure
from dependencies.python.fmlaas import ModelNameType

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

    def test_identify_name_type_1(self):
        name_txt = "1234/5678/5678"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name._identify_name_type(), ModelNameType.ROUND_AGGREGATE_MODEL)

    def test_identify_name_type_2(self):
        name_txt = "1234/1234"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name._identify_name_type(), ModelNameType.INITIAL_GROUP_MODEL)

    def test_identify_name_type_2_fail(self):
        name_txt = "1234/5678"

        name = HierarchicalModelNameStructure()

        self.assertRaises(ValueError, name.load_name, name_txt)

    def test_identify_name_type_3(self):
        name_txt = "1234/5678/9999"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name._identify_name_type(), ModelNameType.DEVICE_MODEL_UPDATE)

    def test_is_round_aggregate_model_1(self):
        name_txt = "1234/5678/9999"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertFalse(name.is_round_aggregate_model())

    def test_is_round_aggregate_model_2(self):
        name_txt = "1234/5678/5678"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name.is_round_aggregate_model())

    def test_is_initial_group_model_1(self):
        name_txt = "1234/5678/9999"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertFalse(name.is_initial_group_model())

    def test_is_initial_group_model_2(self):
        name_txt = "1234/1234"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name.is_initial_group_model())

    def test_is_device_model_update_1(self):
        name_txt = "1234/5678/9999"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name.is_device_model_update())

    def test_is_device_model_update_2(self):
        name_txt = "1234/5678/5678"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertFalse(name.is_device_model_update())
