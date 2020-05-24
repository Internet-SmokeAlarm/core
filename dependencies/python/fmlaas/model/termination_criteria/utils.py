from .duration import DurationTerminationCriteria


def get_termination_criteria_from_json(json_data):
    """
    :param json_data: dict
    """
    return get_termination_criteria_class_from_json(
        json_data).from_json(json_data)


def get_termination_criteria_class_from_json(json_data):
    """
    :param json_data: dict
    """
    if "type" not in json_data:
        raise ValueError("Invalid JSON input")
    elif json_data["type"] == str(DurationTerminationCriteria.__name__):
        return DurationTerminationCriteria

    raise ValueError("Unknown termination criteria type")
