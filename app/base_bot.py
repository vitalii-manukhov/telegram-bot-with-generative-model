from abc import ABC, abstractmethod
from client import Client
from logger import Logger
from models import Message


class Bot(ABC):
    def __init__(self, client: Client):
        self._client = client

        logger_name = self.__class__.__name__.lower() + "_logger"
        self._logger = Logger(logger_name)

    @classmethod
    def run_bot(cls):
        # cls._client.run_server
        cls._logger.info("Bot is up and running")

    @classmethod
    def stop_bot(cls):
        # cls._clinet.stop_server
        cls._logger.info("Bot has been stopped")
        pass

    @abstractmethod
    def process_message(self, message: Message):
        pass
