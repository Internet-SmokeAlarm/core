import torch
import json
import sys
sys.path.append(".")
from bindings.pytorch.python.fmlaas_pytorch.storage import DiskModelStorage

STATE_DICTS_TO_SERIALIZE = ["tests/fmlaas_pytorch/data/mnist_cnn_2.pt", "tests/fmlaas_pytorch/data/mnist_cnn.pt"]
OUTPUT_JSON = ["tests/fmlaas_pytorch/data/mnist_cnn_2.json", "tests/fmlaas_pytorch/data/mnist_cnn.json"]

def serialize_state_dict(path):
    return {key : item.numpy().tolist() for key, item in torch.load(path).items()}

def save_state_dict_to_json_file(path, dictionary):
    with open(path, "w") as f:
        DiskModelStorage.store_model(f, dictionary)

if __name__ == '__main__':
    for state_dict, output_file in zip(STATE_DICTS_TO_SERIALIZE, OUTPUT_JSON):
        serialized_state_dict = serialize_state_dict(state_dict)

        save_state_dict_to_json_file(output_file, serialized_state_dict)
