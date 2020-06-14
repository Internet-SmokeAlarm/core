import numpy


def deserialize_state_dict(state_dict):
    """
    :param state_dict: dictionary
    """
    return {key: numpy.asarray(item, dtype=numpy.float32)
            for key, item in state_dict.items()}
