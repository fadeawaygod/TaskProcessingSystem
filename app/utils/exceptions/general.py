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


@dataclass
class BadRequestWithMessage(BaseCustomException):
    """BadRequestWithMessage."""

    message: str
    _status_code = HTTPStatus.BAD_REQUEST
    _code = 10001
    _message = "Bad Request: {message}."


@dataclass
class NotFoundWithMessage(BaseCustomException):
    """NotFoundWithMessage."""

    message: str
    _status_code = HTTPStatus.NOT_FOUND
    _code = 10002
    _message = "Not Found: {message}."


@dataclass
class ConflicWithMessage(BaseCustomException):
    """ConflicWithMessage."""

    message: str
    _status_code = HTTPStatus.CONFLICT
    _code = 10003
    _message = "Conflict: {message}."


@dataclass
class WsConnectionEmptyError(BaseCustomException):
    """ws connection is empty."""

    _status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    _code = 10004
    _message = "The ws connection is empty."


@dataclass
class WorkspaceUserIsAlreadyActive(BaseCustomException):
    """Workspace User is already active."""

    account: str
    _status_code = HTTPStatus.BAD_REQUEST
    _code = 10005
    _message = "The workspace user {account} is already active."


@dataclass
class CreateWorkspaceUserPermissionError(BaseCustomException):
    """Create Workspace user Permission Error."""

    account: str
    role: str
    _status_code = HTTPStatus.FORBIDDEN
    _code = 10006
    _message = "The workspace user {account} has no permission to create role: {role}."


@dataclass
class UploadFileException(BaseCustomException):
    """An exception occurred while uploading the file."""

    upload_file_name: str
    save_file_name: str
    detail: str
    _status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    _code = 10007
    _message = "Upload the file  {upload_file_name} and save it as an error occurred while {save_file_name}. {detail}"


@dataclass
class ChannelAlreadyBeenSubscribed(BaseCustomException):
    """the channel is already been subscribed."""

    channel: str
    _status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    _code = 10008
    _message = "Channel {channel} is already been subscribed."


@dataclass
class RateLimitExceededError(BaseCustomException):
    """RateLimitExceededError."""

    granularity: str
    _status_code = HTTPStatus.TOO_MANY_REQUESTS
    _code = 10009
    _message = "Requests rate limit of {granularity} exceeded."
