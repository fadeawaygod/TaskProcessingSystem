"""Exceptions of Task, range of error code : 40000~49999.

app code:
400xx: general
"""

from dataclasses import dataclass
from http import HTTPStatus

from .base_custom_exception import BaseCustomException

# general, range of error code : 40000~40099


@dataclass
class TaskRuntimeError(BaseCustomException):
    """TaskRuntimeError."""

    error: str
    _status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    _code = 40000
    _message = "task runtime error: {error}."


@dataclass
class JobCannotBeCancelled(BaseCustomException):
    """JobCannotBeCancelled."""

    current_status: str
    allowed_status: str
    _status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    _code = 40001
    _message = "task cannot be cancelled, current status: {current_status}, allowed status: {allowed_status}."
