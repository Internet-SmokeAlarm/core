from .duration import DurationTerminationCriteria

def get_termination_criteria_from_json(json_data):
    """
    :param json_data: dict
    """
    if "class_name" not in json_data:
        raise ValueError("Invalid JSON input")
    elif json_data["class_name"] == str(DurationTerminationCriteria.__name__):
        return DurationTerminationCriteria.from_json(json_data)

    raise ValueError("Unknown termination criteria type")
