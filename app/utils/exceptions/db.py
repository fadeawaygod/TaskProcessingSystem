"""Exceptions. of db&redis, range of error code : 20000~29999.

app code:
200xx: general
"""

from dataclasses import dataclass
from http import HTTPStatus

from .base_custom_exception import BaseCustomException


# general, range of error code : 20000~20099
@dataclass
class UnknownDatabaseError(BaseCustomException):
    """UnknownDatabaseError."""

    error: str
    _status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    _code = 20000
    _message = "An Database error occurs: {error}."


@dataclass
class EntryWithIDNotExist(BaseCustomException):
    """EntryWithIDNotExist."""

    entry_name: str
    id: str
    _status_code = HTTPStatus.NOT_FOUND
    _code = 20001
    _message = "The entry: {entry_name}, id: {id} does not exist."


@dataclass
class OrderColumnNotExist(BaseCustomException):
    """OrderColumnNotExist."""

    column: str
    _status_code = HTTPStatus.BAD_REQUEST
    _code = 20002
    _message = "The column: {column} used to order does not exist."


@dataclass
class InvalidOrderDirection(BaseCustomException):
    """InvalidOrderDirection."""

    direction: str
    _status_code = HTTPStatus.BAD_REQUEST
    _code = 20003
    _message = "The Direction: {direction} used to order is invalid."
