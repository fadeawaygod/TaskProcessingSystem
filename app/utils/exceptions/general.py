"""Exceptions of general, range of error code : 10000~19999.

app code:
100xx: general
"""

from dataclasses import dataclass
from http import HTTPStatus

from .base_custom_exception import BaseCustomException

# region general, range of error code : 10000~10099


@dataclass
class ErrorCodeDuplicated(BaseCustomException):
    """ErrorCodeDuplicated."""

    code: int
    _status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    _code = 10000
    _message = "The error code: {code} is duplicated"
