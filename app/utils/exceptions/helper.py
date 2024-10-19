from typing import Optional, Union

from .base_custom_exception import BaseCustomException, CodeErrorCollector


def parse_exception(code: int, parameters: Optional[Union[dict, bytes, str]] = None) -> BaseCustomException:
    """Parse exception from exception object or value.

    Args:
        code (int): Exception error code.
        parameters (Union[dict, str, bytes]): Custom exception instantiates with code and parameters. (default: `None`)

    Returns:
        BaseCustomException: Custom exception instantiates with code and parameters.

    Raises:
        ValueError: Invalid code or parameters.
    """
    mapped_exception = CodeErrorCollector.mapping.get(code)
    if not mapped_exception:
        raise ValueError(f"The error code {code} does not exist.")

    try:
        if isinstance(parameters, dict):
            return mapped_exception.parse_obj(parameters)
        else:
            return mapped_exception.parse_raw(parameters)

    except TypeError:
        name = mapped_exception.__name__
        raise ValueError(f"{name} cannot instantiate with parameters {parameters}")
