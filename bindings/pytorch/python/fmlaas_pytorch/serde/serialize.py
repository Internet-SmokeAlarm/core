def serialize_numpy(state_dict):
    """
    Serializes a numpy version of the state dict (i.e. converts all numpy lists to just lists).

    Note: Cannot serialize a Torch state dict (which contains tensors).

    :param state_dict: dictionary
    """
    return {key : item.tolist() for key, item in state_dict.items()}
