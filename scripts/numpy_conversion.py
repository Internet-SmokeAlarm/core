import torch
from loguru import logger
import json

TEST_STATE_DICT = "tests/fmlaas/data/mnist_cnn_2.pt"


def load_state_dict(file_path):
    logger.info("Loading state dict: {}", file_path)

    return torch.load(file_path)


if __name__ == '__main__':
    # TESTING MANIPULATING STATE DICT W/ NUMPY ARRAYS

    state_dict = load_state_dict(TEST_STATE_DICT)

    # print(state_dict)
    print(state_dict.keys())
    print(state_dict["conv1.bias"])
    print(state_dict["conv1.bias"].numpy())
    x = json.dumps(state_dict["conv1.bias"].numpy().tolist())
    print(x)
    y = json.loads(x)
    print(y)
    print(torch.tensor(y))

    print(state_dict["conv1.weight"])
    x = json.dumps(state_dict["conv1.weight"].numpy().tolist())
    print(x)
    y = json.loads(x)
    print(y)
    print(torch.tensor(y))
