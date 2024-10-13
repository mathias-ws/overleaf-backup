import logging
from logging import Formatter, StreamHandler

from overleaf_backup.utils.config import LoggingSettings


def __get_log_level(log_level: str) -> int:
    """
    Translates a str log level into the correct value.

    Valid levels: debug, info, warning and critical

    :param log_level: The log level as a valid string.
    :return: The log level as dictated in the logging library.
    """
    if log_level == "debug":
        return logging.DEBUG
    elif log_level == "info":
        return logging.INFO
    elif log_level == "warning":
        return logging.WARNING
    elif log_level == "critical":
        return logging.CRITICAL
    else:
        logging.warning(f"{log_level} is not a valid log level, defaulting to info.")
        return logging.INFO


def setup_logging(config: LoggingSettings):
    formatter = Formatter(
        fmt="%(asctime)s:%(levelname)s::%(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)

    logging.basicConfig(
        level=__get_log_level(config.level),
        handlers=[stream_handler],
    )