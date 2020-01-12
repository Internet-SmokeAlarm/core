import json

def generate_aggregation_func_payload(group_id, round_id):
    """
    :param group_id: string
    :param round_id: string
    """
    return json.dumps({
        "group_id" : group_id,
        "round_id" : round_id
    })
