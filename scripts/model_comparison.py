import torch
from aggregate_models.app import FashionMNISTCNN
import os
from loguru import logger

MODELS_1_PATH = "/Users/valetolpegin/Downloads/9277325339966456776_15785926002308826036"
MODELS_2_PATH = "/Users/valetolpegin/Downloads/3789502442958572662_15785926002308826036"
MODEL_CLASS = FashionMNISTCNN
NUM_OUTPUTS = 10

def compare_models(model_1, model_2):
    models_differ = 0
    for key_item_1, key_item_2 in zip(model_1.state_dict().items(), model_2.state_dict().items()):
        if torch.equal(key_item_1[1], key_item_2[1]):
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

if __name__ == '__main__':
    # Compares two sets of model systems to see if they are equal.
    # Must have the same architecture in order to compare.

    logger.info("Loading model: {}", MODELS_1_PATH)
    model_1 = MODEL_CLASS(num_outputs=NUM_OUTPUTS)
    model_1.load_state_dict(torch.load(MODELS_1_PATH))

    logger.info("Loading model: {}", MODELS_2_PATH)
    model_2 = MODEL_CLASS(num_outputs=NUM_OUTPUTS)
    model_2.load_state_dict(torch.load(MODELS_2_PATH))

    logger.info("Comparing model parameter...")
    compare_models(model_1, model_2)
