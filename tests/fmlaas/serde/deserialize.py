import unittest
import torch
from torch import tensor
from dependencies.python.fmlaas.serde import deserialize_state_dict
from dependencies.python.fmlaas.storage import DiskModelStorage


class DeserializeStateDictTestCase(unittest.TestCase):

    def test_deserialize_state_dict_1(self):
        state_dict = torch.load("tests/fmlaas/data/mnist_cnn_2.pt")
        with open("tests/fmlaas/data/mnist_cnn_2.json", "r") as f:
            model_1_state_dict = deserialize_state_dict(
                DiskModelStorage.load_model(f))

        for key in state_dict.keys():
            self.assertTrue(
                torch.equal(
                    state_dict[key], tensor(
                        model_1_state_dict[key])))

    def test_deserialize_state_dict_2(self):
        state_dict = torch.load("tests/fmlaas/data/mnist_cnn.pt")
        with open("tests/fmlaas/data/mnist_cnn.json", "r") as f:
            model_2_state_dict = deserialize_state_dict(
                DiskModelStorage.load_model(f))

        for key in state_dict.keys():
            self.assertTrue(
                torch.equal(
                    state_dict[key], tensor(
                        model_2_state_dict[key])))
