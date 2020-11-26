from typing import List

from ..utils.time import get_epoch_time
from .job import Job
from .job_configuration import JobConfiguration
from .status import Status


class JobFactory:

    @staticmethod
    def create_job(id: str,
                   configuration: JobConfiguration,
                   devices: List[str] = []):
        status = Status.INITIALIZED
        aggregate_model = {}
        start_model = {}
        models = {}
        created_at = get_epoch_time()
        billable_size = 0
        testing_reports = {}


        return Job(id,
                   devices,
                   status,
                   aggregate_model,
                   start_model,
                   configuration,
                   models,
                   created_at,
                   billable_size,
                   testing_reports)
