from ...database import DB
from ...model import DBObject
from ...model import Job
from ...model import Model
from ...model import Project
from ...model import JobStatus
from ...s3_storage import PointerFactory
from ...s3_storage import PointerType
from ...aws import trigger_lambda_function
from ...utils import get_aggregation_lambda_func_name
from ..utils import update_experiment
from .lambda_trigger_helper import generate_aggregation_func_payload


def models_uploaded_controller(project_db: DB, job_db: DB, models_uploaded):
    """
    :param models_uploaded: list(string)
    """
    for model in models_uploaded:
        handler_function = get_model_process_function(str(model.get_name()))
        should_trigger_aggregation = handler_function(
            model, project_db, job_db)

        if should_trigger_aggregation:
            payload = generate_aggregation_func_payload(
                model_name.get_job_id())

            trigger_lambda_function(
                get_aggregation_lambda_func_name(), payload)


def get_model_process_function(model_name: str):
    pointer_type = PointerFactory.get_pointer_type(model_name)

    if pointer_type == PointerType.EXPERIMENT_START_MODEL:
        return handle_experiment_start_model
    elif pointer_type == PointerType.DEVICE_MODEL_UPDATE:
        return handle_device_model_update
    elif pointer_type == PointerType.JOB_AGGREGATE_MODEL:
        return handle_job_aggregate_model


def handle_experiment_start_model(model: Model, project_db: DB, job_db: DB):
    model.set_entity_id(model.get_name().experiment_id)

    project = DBObject.load_from_db(Project, model.get_name().project_id, project_db)
    experiment = project.get_experiment(model.get_name().experiment_id)
    experiment.start_model = model
    project.add_or_update_experiment(experiment)
    project.save_to_db(job_db)

    return False


def handle_device_model_update(model: Model, project_db: DB, job_db: DB):
    model.set_entity_id(model.get_name().device_id)

    job = DBObject.load_from_db(Job, model.get_name().job_id, job_db)
    job.add_model(model)

    should_aggregate = not job.is_aggregation_in_progress() and job.should_aggregate()
    if should_aggregate:
        job.set_status(JobStatus.AGGREGATION_IN_PROGRESS)

    job.save_to_db(job_db)

    return should_aggregate


def handle_job_aggregate_model(model: Model, project_db: DB, job_db: DB):
    model.set_entity_id(model.get_name().job_id)

    job = DBObject.load_from_db(Job, model.get_name().job_id, job_db)
    job.set_aggregate_model(model)
    job.complete()
    job.save_to_db(job_db)

    update_experiment(job, job_db, project_db)
