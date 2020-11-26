from typing import List

from .duration import DurationTerminationCriteria
from .termination_criteria import TerminationCriteria


def load_termination_criteria_from_json(json_data: List) -> List[TerminationCriteria]:
    termination_criteria = list()
    for criteria in json_data:
        termination_criteria.append(get_termination_criteria_from_json(criteria))
    
    return termination_criteria


def save_termination_criteria_to_json(termination_criteria: List[TerminationCriteria]) -> List[dict]:
    json_data = list()
    for criteria in termination_criteria:
        json_data.append(criteria.to_json())
    
    return json_data


def get_termination_criteria_from_json(json_data: dict) -> TerminationCriteria:
    return get_termination_criteria_class_from_json(
        json_data).from_json(json_data)


def get_termination_criteria_class_from_json(json_data: dict) -> TerminationCriteria:
    if "type" not in json_data:
        raise ValueError("Invalid JSON input")
    elif json_data["type"] == str(DurationTerminationCriteria.__name__):
        return DurationTerminationCriteria

    raise ValueError("Unknown termination criteria type")
