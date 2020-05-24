from bindings.pytorch.python.fmlaas_pytorch.storage import DiskModelStorage
from bindings.pytorch.python.fmlaas_pytorch.serde import deserialize_state_dict
from bindings.pytorch.python.fmlaas_pytorch import scale_model
from bindings.pytorch.python.fmlaas_pytorch import combine_models
import os
from loguru import logger
import sys
import numpy
sys.path.append(".")

STATE_DICTS_TO_COMBINE_PATH = [
    "tests/fmlaas/data/mnist_cnn_2.json",
    "tests/fmlaas/data/mnist_cnn.json"]
STATE_DICT_COMBINED_PATH = "/Users/valetolpegin/Downloads/1320626241526138"


def compare_state_dicts(model_1, model_2):
    models_differ = 0
    for key_item_1, key_item_2 in zip(model_1.items(), model_2.items()):
        if numpy.all(key_item_1[1] == key_item_2[1]):
            pass
        else:
            models_differ += 1
            if (key_item_1[0] == key_item_2[0]):
                logger.error('Mismatch found at {}', key_item_1[0])
                logger.debug("Model 1 value: {}", str(key_item_1[1]))
                logger.debug("Model 2 value: {}", str(key_item_2[1]))
            else:
                raise Exception
    if models_differ == 0:
        logger.info('Models match perfectly!')


def load_state_dict(file_path):
    logger.info("Loading state dict: {}", file_path)

    with open(file_path, "r") as f:
        return deserialize_state_dict(DiskModelStorage.load_model(f))


if __name__ == '__main__':
    combined_state_dict = load_state_dict(STATE_DICT_COMBINED_PATH)

    combined_model = load_state_dict(STATE_DICTS_TO_COMBINE_PATH[0])
    for state_dict_to_combine in STATE_DICTS_TO_COMBINE_PATH[1:]:
        state_dict = load_state_dict(state_dict_to_combine)

        combined_model = combine_models(combined_model, state_dict)

    scaled_model = scale_model(
        combined_model,
        len(STATE_DICTS_TO_COMBINE_PATH))

    logger.info("Comparing state dict...")
    compare_state_dicts(combined_state_dict, scaled_model)
