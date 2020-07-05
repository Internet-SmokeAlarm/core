from dataclasses import dataclass
from .s3_object_pointer import S3ObjectPointer


@dataclass(frozen=True)
class DeviceModelPointer(S3ObjectPointer):

    project_id: str
    experiment_id: str
    job_id: str
    device_id: str

    def __str__(self) -> str:
        return self.project_id + \
               S3ObjectPointer.DELIMITER + \
               self.experiment_id + \
               S3ObjectPointer.DELIMITER + \
               self.job_id + \
               S3ObjectPointer.DELIMITER + \
               "device_models" + \
               S3ObjectPointer.DELIMITER + \
               self.device_id

    @staticmethod
    def from_str(str_rep):
        parts = str_rep.split(S3ObjectPointer.DELIMITER)

        project_id = parts[0]
        experiment_id = parts[1]
        job_id = parts[2]
        device_id = parts[4]

        return DeviceModelPointer(project_id, experiment_id, job_id, device_id)
