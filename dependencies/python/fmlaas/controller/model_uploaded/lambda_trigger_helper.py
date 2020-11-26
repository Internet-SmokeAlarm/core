import json


def generate_aggregation_func_payload(project_id: str, experiment_id: str, job_id: str) -> dict:
    return json.dumps({
        "project_id": project_id,
        "experiment_id": experiment_id,
        "job_id": job_id
    })
