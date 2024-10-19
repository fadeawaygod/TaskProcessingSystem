from enum import Enum


class TaskStatus(str, Enum):
    """ """

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskType(str, Enum):
    """ """

    SLEEP = "SLEEP"
