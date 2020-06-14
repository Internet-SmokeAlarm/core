from ...model import DBObject
from ...model import Project
from ...model import Job
from ...database import DB


def update_experiment(current_job: Job, job_db: DB, project_db: DB):
    project = DBObject.load_from_db(
        Project, current_job.get_project_id(), project_db)

    experiment = project.get_experiment(current_job.get_experiment_id())
    experiment.current_model = current_job.get_end_model()

    experiment.proceed_to_next_job()
    while experiment.is_active:
        job = DBObject.load_from_db(Job, experiment.current_job, job_db)
        if not job.is_cancelled():
            job.set_start_model(experiment.current_model)
            job.reset_termination_criteria()
            job.save_to_db(job_db)

            break

        experiment.proceed_to_next_job()

    project.add_or_update_experiment(experiment)
    project.save_to_db(project_db)


def termination_check(current_job: Job, job_db: DB, project_db: DB):
    """
    Checks to see whether or not the current job should be terminated. If so,
    handle termination, and update.
    """
    is_terminated = current_job.should_terminate()

    if is_terminated:
        current_job.cancel()

        update_experiment(current_job, job_db, project_db)

        current_job.save_to_db(job_db)

    return is_terminated
