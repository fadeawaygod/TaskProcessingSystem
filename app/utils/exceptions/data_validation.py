"""Exceptions of data validation, range of error code : 30000~39999.

app code:
300xx: general
"""

from dataclasses import dataclass
from http import HTTPStatus

from .base_custom_exception import BaseCustomException

# general, range of error code : 30000~39999


@dataclass
class InvalidDataFormatError(BaseCustomException):
    """InvalidDataFormatError."""

    _status_code = HTTPStatus.BAD_REQUEST
    _code = 30000
    _message = "The data format is invalid."


@dataclass
class InvalidContentTypeError(BaseCustomException):
    """InvalidContentTypeError."""

    content_type: str
    _status_code = HTTPStatus.BAD_REQUEST
    _code = 30001
    _message = "The content type: {content_type} is invalid."


@dataclass
class MissingParameterInHeaderError(BaseCustomException):
    """MissingParameterInHeaderError."""

    key: str
    _status_code = HTTPStatus.BAD_REQUEST
    _code = 30002
    _message = "Missing {key} in header"


@dataclass
class MissRequiredParameterError(BaseCustomException):
    """MissRequiredParameterError."""

    parameter: str
    _status_code = HTTPStatus.BAD_REQUEST
    _code = 30003
    _message = "the required parameter: {parameter} is missing"


@dataclass
class ParameterTypeInvalidError(BaseCustomException):
    """ParameterTypeInvalidError."""

    parameter: str
    valid_type: str
    invalid_type: str
    _status_code = HTTPStatus.BAD_REQUEST
    _code = 30004
    _message = "the type parameter: {parameter} is expected to {valid_type}, got {invalid_type}."


@dataclass
class ParameterNotInEnumError(BaseCustomException):
    """ParameterNotInEnumError."""

    parameter: str
    enum: str
    _status_code = HTTPStatus.BAD_REQUEST
    _code = 30005
    _message = "the parameter: {parameter} is not in enum: {enum}."


@dataclass
class NoValidPatchKeyError(BaseCustomException):
    """NoValidPatchKeyError."""

    _status_code = HTTPStatus.BAD_REQUEST
    _code = 30006
    _message = "there is no valid key in body."


@dataclass
class UnexpectedParameterInError(BaseCustomException):
    """UnexpectedParameterInError."""

    parameter: str
    target: str
    _status_code = HTTPStatus.BAD_REQUEST
    _code = 30007
    _message = "the parameter: {parameter} is unexpected in {target}."


@dataclass
class DuplicateDataError(BaseCustomException):
    """DuplicateDataError."""

    data: str
    _status_code = HTTPStatus.BAD_REQUEST
    _code = 30008
    _message = "The data {data} is duplicated."
