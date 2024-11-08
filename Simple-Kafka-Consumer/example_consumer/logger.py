import datetime
import logging
import sys
from typing import Optional

from pythonjsonlogger import jsonlogger

from example_consumer.config import LOG_LEVEL

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


class EventJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        # log_record is an OrderedDict, so this order matters (for visual purposes)
        log_record['timestamp'] = datetime.datetime.fromtimestamp(record.created)
        log_record['level'] = record.levelname
        log_record['message'] = record.message
        log_record['logger_name'] = record.name
        log_record['file_location'] = "{}:{}".format(record.pathname, record.lineno)
        super(EventJsonFormatter, self).add_fields(log_record, record, message_dict)


class LogMixin:
    _logger: Optional[logging.Logger]

    def __init__(self):
        self._logger = None

    @property
    def logger(self):
        if not self._logger:
            self._logger = get_logger(self.__class__.__name__)

        return self._logger


def get_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)

    # create formatter and handler if not exists
    if not logger.hasHandlers():
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        file_handler = logging.FileHandler("./logs/" + datetime.datetime.now().strftime("run_%Y-%m-%d-%H-%M.log"))
        event_json_formatter = EventJsonFormatter()
        stdout_handler.setFormatter(event_json_formatter)
        file_handler.setFormatter(event_json_formatter)
        logger.setLevel(LOG_LEVELS.get(LOG_LEVEL))
        logger.addHandler(stdout_handler)
        logger.addHandler(file_handler)

    return logger
