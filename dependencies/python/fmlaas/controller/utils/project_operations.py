from ...model import DBObject
from ...model import Project
from ...model import Job

def update_job_path(current_job, job_db, project_db):
    """
    Removes the current_job object from a project's active jobs, identifies
    the next job that should be initialized in sequence (if any), and activates it.

    :param current_job: Job
    :param job_db: DB
    :param project_db: DB
    """
    project = DBObject.load_from_db(Project, current_job.get_parent_project_id(), project_db)
    project.remove_current_job_id(current_job.get_id())

    job_id = project.get_next_job_in_sequence(current_job.get_id())
    while job_id is not None:
        job = DBObject.load_from_db(Job, job_id, job_db)
        if not job.is_cancelled():
            project.add_current_job_id(job_id)

            job.set_start_model(current_job.get_end_model())
            job.reset_termination_criteria()
            job.save_to_db(job_db)

            break

        job_id = project.get_next_job_in_sequence(job_id)

    project.save_to_db(project_db)

    return

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

        update_job_path(current_job, job_db, project_db)

        current_job.save_to_db(job_db)
