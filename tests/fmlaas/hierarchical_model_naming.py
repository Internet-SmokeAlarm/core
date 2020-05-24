import unittest

from dependencies.python.fmlaas import HierarchicalModelNameStructure
from dependencies.python.fmlaas import ModelNameType

class HierarchicalModelNameStructureTestCase(unittest.TestCase):

    def test_generate_name_pass(self):
        job_id = "44563"
        device_id = "6665"

        name = HierarchicalModelNameStructure()
        name.generate_name(is_start_model=False, job_id=job_id, device_id=device_id)

        self.assertEqual("44563/device_models/6665", name.get_name())

    def test_generate_name_2_pass(self):
        name = HierarchicalModelNameStructure()
        name.generate_name(is_start_model=True, job_id="1234")

        self.assertEqual("1234/start_model", name.get_name())

    def test_generate_name_3_pass(self):
        name = HierarchicalModelNameStructure()
        name.generate_name(is_start_model=False, job_id="12353")

        self.assertEqual("12353/aggregate_model", name.get_name())

    def test_generate_device_model_update_name_pass(self):
        job_id = "445634"
        device_id = "6665"

        name = HierarchicalModelNameStructure()
        generated_name = name._generate_device_model_update_name(job_id, device_id)

        self.assertEqual("445634/device_models/6665", generated_name)

    def test_generate_job_start_model_name_pass(self):
        name = HierarchicalModelNameStructure()
        generated_name = name._generate_job_start_model_name(job_id="1234554")

        self.assertEqual("1234554/start_model", generated_name)

    def test_generate_job_aggregate_model_name_pass(self):
        name = HierarchicalModelNameStructure()
        generated_name = name._generate_job_aggregate_model_name(job_id="44563")

        self.assertEqual("44563/aggregate_model", generated_name)

    def test_get_job_id_pass(self):
        name_txt = "44563/aggregate_model"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertEqual(name.get_job_id(), "44563")

    def test_get_device_id_pass(self):
        name_txt = "445634/device_models/6665"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertEqual(name.get_device_id(), "6665")

    def test_identify_name_type_1_pass(self):
        name_txt = "445634/device_models/6665"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name._identify_name_type(), ModelNameType.DEVICE_MODEL_UPDATE)

    def test_identify_name_type_2_pass(self):
        name_txt = "445634/aggregate_model"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name._identify_name_type(), ModelNameType.JOB_AGGREGATE_MODEL)

    def test_identify_name_type_3_pass(self):
        name_txt = "445634/start_model"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name._identify_name_type(), ModelNameType.JOB_START_MODEL)

    def test_is_job_aggregate_model_1_pass(self):
        name_txt = "445634/aggregate_model"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name.is_job_aggregate_model())

    def test_is_job_aggregate_model_2_pass(self):
        name_txt = "445634/start_model"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertFalse(name.is_job_aggregate_model())

    def test_is_device_model_update_1_pass(self):
        name_txt = "445634/device_models/1235234"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name.is_device_model_update())

    def test_is_device_model_update_2_pass(self):
        name_txt = "445634/aggregate_model"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertFalse(name.is_device_model_update())

    def test_is_job_start_model_1_pass(self):
        name_txt = "445634/aggregate_model"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertFalse(name.is_job_start_model())

    def test_is_job_start_model_2_pass(self):
        name_txt = "445634/start_model"

        name = HierarchicalModelNameStructure()
        name.load_name(name_txt)

        self.assertTrue(name.is_job_start_model())
