"""Exceptions of Job, range of error code : 60000~69999.

app code:
600xx: general
603xx: Nearme
"""

from dataclasses import dataclass
from http import HTTPStatus

from .base_custom_exception import BaseCustomException

# general, range of error code : 60000~60099


@dataclass
class JobRuntimeError(BaseCustomException):
    """ScraperTaskRuntimeError."""

    error: str
    _status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    _code = 60000
    _message = "job runtime error: {error}."
