from .s3_object_pointer import S3ObjectPointer
from .device_model import DeviceModelPointer
from .job_aggregate_model import JobAggregateModelPointer
from .experiment_start_model import StartModelPointer
from .pointer_type import PointerType


class PointerFactory:

    @staticmethod
    def load_pointer(str_repr: str) -> S3ObjectPointer:
        pointer_type = PointerFactory.get_pointer_type(str_repr)

        if pointer_type == PointerType.EXPERIMENT_START_MODEL:
            return StartModelPointer.from_str(str_repr)
        elif pointer_type == PointerType.JOB_AGGREGATE_MODEL:
            return JobAggregateModelPointer.from_str(str_repr)
        elif pointer_type == PointerType.DEVICE_MODEL_UPDATE:
            return DeviceModelPointer.from_str(str_repr)

    @staticmethod
    def get_pointer_type(str_repr: str) -> PointerType:
        num_components = len(str_repr.split(S3ObjectPointer.DELIMITER))

        if num_components == 3:
            return PointerType.EXPERIMENT_START_MODEL
        elif num_components == 4:
            return PointerType.JOB_AGGREGATE_MODEL
        elif num_components == 5:
            return PointerType.DEVICE_MODEL_UPDATE
