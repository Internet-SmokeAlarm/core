from enum import Enum


class JobStatus(Enum):

    INITIALIZED = "INITIALIZED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    AGGREGATION_IN_PROGRESS = "AGGREGATION_IN_PROGRESS"
