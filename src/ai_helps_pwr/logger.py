import logging
from pathlib import Path
from typing import Literal, Optional, Union

LOGGER_NAME = "ai_helps_pwr"
LOG_LEVEL_TYPE = Literal[
    "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
]


def initialize_logging(
    logger_to_init: logging.Logger,
    log_level: LOG_LEVEL_TYPE = "INFO",
    file_path: Optional[Union[str, Path]] = None,
):
    """Initialize logger with stdout handler and option file handler."""
    logger_to_init.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger_to_init.addHandler(stream_handler)

    if file_path is not None:
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        logger_to_init.addHandler(file_handler)


def custom_logger(
    logger_name: str,
    log_level: LOG_LEVEL_TYPE = "INFO",
    file_path: Optional[Union[str, Path]] = None,
) -> logging.Logger:
    """Create and initialize custom logger."""
    custom_logger_obj = logging.getLogger(logger_name)
    initialize_logging(custom_logger_obj, log_level, file_path)
    return custom_logger_obj


logger = logging.getLogger(LOGGER_NAME)
initialize_logging(logger)
logger.setLevel(logging.DEBUG)
