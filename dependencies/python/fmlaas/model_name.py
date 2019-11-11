def generate_model_object_name(device_id, round_number):
    """
    Generates appropriate S3 object name given information.

    :param device_id: int
    :param round_number: int
    """
    return str(device_id) + "_" + str(round_number)
