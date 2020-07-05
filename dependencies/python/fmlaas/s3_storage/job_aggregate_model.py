from .s3_object_pointer import S3ObjectPointer
from dataclasses import dataclass


@dataclass(frozen=True)
class JobAggregateModelPointer(S3ObjectPointer):

    project_id: str
    experiment_id: str
    job_id: str

    def __str__(self) -> str:
        return self.project_id + \
               S3ObjectPointer.DELIMITER + \
               self.experiment_id + \
               S3ObjectPointer.DELIMITER + \
               self.job_id + \
               S3ObjectPointer.DELIMITER + \
               "aggregate_model"

    @staticmethod
    def from_str(str_rep):
        parts = str_rep.split(S3ObjectPointer.DELIMITER)

        project_id = parts[0]
        experiment_id = parts[1]
        job_id = parts[2]

        return JobAggregateModelPointer(project_id, experiment_id, job_id)
