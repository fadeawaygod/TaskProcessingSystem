import logging
import os
from enum import Enum
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from typing import Iterable, List, Optional


class LogLevel(str, Enum):
    """LogLevel in case-insensitive."""

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"

    @classmethod
    def _missing_(cls, value: object):
        if not isinstance(value, str):
            raise TypeError(f"Invalid LogLevel value type: {type(value)}")

        value_key = {v: k for v, k in cls.__members__.items()}
        key = value_key.get(value.upper())
        if key:
            return cls.__members__[key]
        else:
            return cls.DEBUG


LOGGER_NAME = "logger"
LOG_LEVEL = LogLevel(os.getenv("LOG_LEVEL", "")).value
LOG_FMT = "[%(asctime)s.%(msecs)03d][%(levelname)s][%(module)s][%(funcName)s,%(lineno)s]: %(message)s"
CONFIG = {"version": 1, "disable_existing_loggers": False}
dictConfig(CONFIG)
formatter = logging.Formatter(LOG_FMT, "%Y-%m-%dT%H:%M:%S")


class CustomStreamHandler(logging.StreamHandler):
    """CustomStreamHandler."""

    def emit(self, record):
        try:
            record.msg = record.msg.replace("\n", "\\n")
            msg = self.format(record)
            stream = self.stream
            stream.write(msg + self.terminator)
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)


def setup_log_handler(handler: logging.Handler, level: LogLevel = LOG_LEVEL, formatter: logging.Formatter = formatter):
    """Set up the handler with level and formatter."""
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def try_add_handler(logger: logging.Logger, handler: logging.Handler):
    """Add the handler if it does not exist."""
    hdlr_names = [h.__class__.__name__ for h in logger.handlers]
    if handler.__class__.__name__ not in hdlr_names:
        logger.addHandler(handler)


def get_logger(stream: bool = True, file: bool = False, handlers: List[logging.Handler] = None) -> logging.Logger:
    """Get the logger and support additional custom handlers in different classes."""
    logger = logging.getLogger(name=LOGGER_NAME)
    logger.propagate = False
    logger.setLevel(LOG_LEVEL)

    if stream:
        try_add_handler(logger, setup_log_handler(CustomStreamHandler()))

    if file:
        try_add_handler(logger, setup_log_handler(RotatingFileHandler(f"{LOGGER_NAME}.log")))

    if handlers:
        for hdlr in handlers:
            try_add_handler(logger, hdlr)

    return logger


def wrap_logger_handlers(name: str, handlers: List[logging.Handler], filters: Optional[List[logging.Filter]] = None):
    """Wrap the specified logger by logger.

    Args:
        name (str): Logger name.
        handlers (List[logging.Handler]): Wrapped handlers for this logger.
        filters (List[logging.Filter]): Additional filters to this logger. (default: `None`)
    """
    _logger = logging.getLogger(name)
    _logger.handlers = handlers
    if isinstance(filters, Iterable):
        [_logger.addFilter(f) for f in filters]
