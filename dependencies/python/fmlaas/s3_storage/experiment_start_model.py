from dataclasses import dataclass
from .s3_object_pointer import S3ObjectPointer


@dataclass(frozen=True)
class StartModelPointer(S3ObjectPointer):

    project_id: str
    experiment_id: str

    def __str__(self) -> str:
        return self.project_id + \
               S3ObjectPointer.DELIMITER + \
               self.experiment_id + \
               S3ObjectPointer.DELIMITER + \
               "start_model"

    @staticmethod
    def from_str(str_rep):
        parts = str_rep.split(S3ObjectPointer.DELIMITER)

        project_id = parts[0]
        experiment_id = parts[1]

        return StartModelPointer(project_id, experiment_id)
