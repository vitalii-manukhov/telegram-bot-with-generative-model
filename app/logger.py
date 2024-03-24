import logging
from config import settings


class Logger:
    def __init__(self, logger_name: str):
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(logging.INFO)
        handler = logging.FileHandler(settings.LOGGER_PATH)
        handler.setLevel(logging.INFO)
        self._logger.addHandler(handler)

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def critical(self, message: str):
        self._logger.critical(message)
