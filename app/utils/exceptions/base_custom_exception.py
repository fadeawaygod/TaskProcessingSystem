"""Base of custom exception."""

import json
from typing import Any, Dict, Optional, Type, TypeVar, Union

BaseCustomExceptionModel = TypeVar("BaseCustomExceptionModel", bound="BaseCustomException")


class CodeErrorCollector(type):
    """Run every time when a class inherited when metaclass CodeErrorCollector.

    The purpose of this class is get the custom exception based on class attribute 'code'.

    for example,
    ```
    error = CodeErrorCollector.mapping[data["code"]]
    raise error(**data["parameters"])
    ```
    """

    mapping: Dict[int, Type["BaseCustomException"]] = {}

    def __new__(cls, name, bases, kwarg):
        new_cls = super().__new__(cls, name, bases, kwarg)
        error_code = kwarg.get("_code")
        if error_code is None:
            return new_cls
        if error_code in cls.mapping:
            raise Exception(f"Error code: {kwarg['code']} is duplicated.")
        cls.mapping[error_code] = new_cls
        return new_cls


class BaseCustomException(Exception, metaclass=CodeErrorCollector):
    """Base of custom exception, it helps the client side to stringify error."""

    _status_code = None
    _code = None
    _message = None

    def __post_init__(self):
        if not hasattr(self, "_message") or not isinstance(self._message, str):
            raise NotImplementedError("Attribute '_message: str' must be set")

        if not hasattr(self, "_code") or not (isinstance(self._code, int) and 99999 > self._code >= 10000):
            raise NotImplementedError("Attribute '_code: int' must be set and range is from 10000 to 99999")

        if not hasattr(self, "_status_code") or not isinstance(self._status_code, int):
            raise NotImplementedError("Attribute '_status_code: int' must be set")

        self.parameters = {
            attr: getattr(self, attr)
            for attr in dir(self)
            if not attr.startswith("_") and attr not in ("args", "with_traceback", "dict", "parse_obj", "parse_raw")
        }
        self.message = self._message.format(**self.parameters)
        self.code = self._code
        self.status_code = self._status_code

    def dict(self) -> dict:
        """Convert to dict."""
        return {
            "message": self.message,
            "code": self.code,
            "status_code": self.status_code,
            "parameters": self.parameters,
        }

    @classmethod
    def parse_obj(cls: Type["BaseCustomExceptionModel"], obj: Optional[Dict[str, Any]] = None) -> "BaseCustomException":
        return cls(**obj) if obj else cls()

    @classmethod
    def parse_raw(cls: Type["BaseCustomExceptionModel"], value: Optional[Union[bytes, str]] = None) -> "BaseCustomException":
        if value:
            obj = json.loads(value)
        else:
            obj = {}

        return cls(**obj) if obj else cls()

    def __str__(self):
        return self.message
