from ...model import DBObject
from ...model import Job
from ...model import JobStatus
from ...aws import trigger_lambda_function
from ...utils import get_aggregation_lambda_func_name
from ..utils import update_job_path
from .lambda_trigger_helper import generate_aggregation_func_payload

def models_uploaded_controller(project_db, job_db, models_uploaded):
    """
    :param project_db: DB
    :param job_db: DB
    :param models_uploaded: list(string)
    """
    for model in models_uploaded:
        model_name = model.get_name()
        handler_function = get_model_process_function(model_name)
        should_trigger_aggregation = handler_function(model, project_db, job_db)

        if should_trigger_aggregation:
            payload = generate_aggregation_func_payload(model_name.get_job_id())

            trigger_lambda_function(get_aggregation_lambda_func_name(), payload)

def get_model_process_function(model_name):
    if model_name.is_job_start_model():
        return handle_job_start_model
    elif model_name.is_device_model_update():
        return handle_device_model_update
    elif model_name.is_job_aggregate_model():
        return handle_job_aggregate_model

def handle_job_start_model(model, project_db, job_db):
    model.set_entity_id(model.get_name().get_job_id())

    job = DBObject.load_from_db(Job, model.get_entity_id(), job_db)
    job.set_start_model(model)
    job.save_to_db(job_db)

    return False

def handle_device_model_update(model, project_db, job_db):
    model.set_entity_id(model.get_name().get_device_id())

    job = DBObject.load_from_db(Job, model.get_name().get_job_id(), job_db)
    job.add_model(model)

    should_aggregate = not job.is_aggregation_in_progress() and job.should_aggregate()
    if should_aggregate:
        job.set_status(JobStatus.AGGREGATION_IN_PROGRESS)

    job.save_to_db(job_db)

    return should_aggregate

def handle_job_aggregate_model(model, project_db, job_db):
    model.set_entity_id(model.get_name().get_job_id())

    job = DBObject.load_from_db(Job, model.get_name().get_job_id(), job_db)
    job.set_aggregate_model(model)
    job.complete()
    job.save_to_db(job_db)

    update_job_path(job, job_db, project_db)
