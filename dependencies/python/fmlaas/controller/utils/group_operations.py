from ...model import DBObject
from ...model import FLGroup
from ...model import Job

def update_job_path(current_job, job_db, group_db):
    """
    Removes the current_job object from a group's active jobs, identifies
    the next job that should be initialized in sequence (if any), and activates it.

    :param current_job: Job
    :param job_db: DB
    :param group_db: DB
    """
    group = DBObject.load_from_db(FLGroup, current_job.get_parent_group_id(), group_db)
    group.remove_current_job_id(current_job.get_id())

    job_id = group.get_next_job_in_sequence(current_job.get_id())
    while job_id is not None:
        job = DBObject.load_from_db(Job, job_id, job_db)
        if not job.is_cancelled():
            group.add_current_job_id(job_id)

            job.set_start_model(current_job.get_end_model())
            job.reset_termination_criteria()
            job.save_to_db(job_db)

            break

        job_id = group.get_next_job_in_sequence(job_id)

    group.save_to_db(group_db)

    return

def termination_check(current_job, job_db, group_db):
    """
    Checks to see whether or not the current job should be terminated. If so,
    handle termination, and update.

    :param current_job: Job
    :param job_db: DB
    :param group_db: DB
    """
    if current_job.should_terminate():
        current_job.cancel()

        update_job_path(current_job, job_db, group_db)

        current_job.save_to_db(job_db)
