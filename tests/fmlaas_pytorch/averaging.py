import unittest
import torch
import os
from torch import tensor
import json
import numpy

from bindings.pytorch.python.fmlaas_pytorch import combine_models
from bindings.pytorch.python.fmlaas_pytorch import scale_model
from bindings.pytorch.python.fmlaas_pytorch.serde import deserialize_state_dict
from bindings.pytorch.python.fmlaas_pytorch.storage import DiskModelStorage

class AveragingTestCase(unittest.TestCase):

    def test_combine_models(self):
        with open("tests/fmlaas_pytorch/data/mnist_cnn_2.json", "r") as f:
            model_1_state_dict = deserialize_state_dict(DiskModelStorage.load_model(f))
        with open("tests/fmlaas_pytorch/data/mnist_cnn.json", "r") as f:
            model_2_state_dict = deserialize_state_dict(DiskModelStorage.load_model(f))

        combined_model = combine_models(model_1_state_dict, model_2_state_dict)

        self.assertTrue(
            torch.equal(tensor([-0.21135749, 0.07840048, 0.05335266, -0.10105486, 0.17683682]),
            tensor(combined_model["conv1.bias"])))

    def test_scale_model(self):
        with open("tests/fmlaas_pytorch/data/mnist_cnn_2.json", "r") as f:
            model_1_state_dict = deserialize_state_dict(DiskModelStorage.load_model(f))
        with open("tests/fmlaas_pytorch/data/mnist_cnn.json", "r") as f:
            model_2_state_dict = deserialize_state_dict(DiskModelStorage.load_model(f))

        combined_model = combine_models(model_1_state_dict, model_2_state_dict)
        scaled_model = scale_model(combined_model, 2)

        self.assertTrue(
            torch.equal(tensor([-0.105678745, 0.03920024, 0.02667633, -0.05052743, 0.08841841]),
            tensor(scaled_model["conv1.bias"])))
