import json


def generate_aggregation_func_payload(job_id):
    """
    :param job_id: string
    """
    return json.dumps({
        "job_id": job_id
    })
