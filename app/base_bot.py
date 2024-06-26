from app.client import Client
from app.logger import Logger

from aiohttp import ClientResponseError
from abc import ABC, abstractmethod
from utils.models import Message


class Bot(ABC):
    def __init__(self):
        client = Client()
        self._client = client

        logger_name = self.__class__.__name__.lower() + "_logger"
        self._logger = Logger(logger_name)

    def run_bot(self):
        self._logger.info("Bot is up and running")
        self._client.set_webhook()
        self._logger.info("Webhook set")

        try:
            self._logger.info("Server is up and running")
            self._client.run_server()
        except ClientResponseError as exception:
            self._logger.error(exception)

    @classmethod
    def stop_bot(cls):
        cls._client.stop_server()
        cls._logger.info("Bot has been stopped")

    @abstractmethod
    def process_message(self, message: Message):
        pass
