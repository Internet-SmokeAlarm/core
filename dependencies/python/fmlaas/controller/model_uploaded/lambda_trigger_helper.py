import json

def generate_aggregation_func_payload(round_id):
    """
    :param round_id: string
    """
    return json.dumps({
        "round_id" : round_id
    })
