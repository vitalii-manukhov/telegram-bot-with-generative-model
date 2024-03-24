from base_bot import Bot
from models import Message
from database import DataBase
from client import Client


class TelegramBot(Bot):
    def __init__(self, client: Client, database: DataBase):
        super().__init__(client)
        self._database = database

    def process_message(self, message: Message):
        """..."""
