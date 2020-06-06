from ...model import DBObject
from ...model import Project
from ...model import Job


def update_job_sequence(current_job, job_db, project_db):
    """
    :param current_job: Job
    :param job_db: DB
    :param project_db: DB
    """
    project = DBObject.load_from_db(
        Project, current_job.get_parent_project_id(), project_db)

    job_sequence = project.get_job_sequence(current_job.get_parent_job_sequence_id())

    job_sequence.proceed_to_next_job()
    while job_sequence.is_active:
        job = DBObject.load_from_db(Job, job_sequence.current_job, job_db)
        if not job.is_cancelled():
            job.set_start_model(job_sequence.current_model)
            job.reset_termination_criteria()
            job.save_to_db(job_db)

            break

        job_sequence.proceed_to_next_job()

    project.add_or_update_job_sequence(job_sequence)
    project.save_to_db(project_db)


def termination_check(current_job, job_db, project_db):
    """
    Checks to see whether or not the current job should be terminated. If so,
    handle termination, and update.

    :param current_job: Job
    :param job_db: DB
    :param project_db: DB
    """
    if current_job.should_terminate():
        current_job.cancel()

        update_job_sequence(current_job, job_db, project_db)

        current_job.save_to_db(job_db)
