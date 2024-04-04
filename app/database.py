from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table
from sqlalchemy import select

from config import settings
from models import Update, metadata_object
from typing import Dict, Any


class DataBase:
    def __init__(self):
        self._engine = create_engine(url=settings.url_for_db,
                                     echo=True)
        self._session = sessionmaker(self._engine)
        self._metadata = metadata_object

    @classmethod
    def get_table(cls, table_name):
        return Table(table_name, cls._metadata, autoload_with=cls._engine)

    def record_update(self, update: Update):
        with self._engine.connect() as conn:
            with self._session(bind=conn) as session:
                data = {
                    "update_id": update.update_id,
                    "message_id": update.message.message_id,
                    "user_id": update.message.from_user.user_id,
                    "is_bot": update.message.from_user.is_bot,
                    "first_name": update.message.from_user.first_name,
                    "username": update.message.from_user.username,
                    "language_code": update.message.from_user.language_code,
                    "chat_id": update.message.chat.chat_id,
                    "chat_type": update.message.chat.chat_type,
                    "date": update.message.date,
                    "text": update.message.text
                }
                session.add(data)
                session.commit()

            conn.commit()

    def record_bot_reply(self, data: Dict[str, Any]):
        with self._engine.connect() as conn:
            with self._session(bind=conn) as session:
                session.add(data)
                session.commit()

            conn.commit()

    def read_data(self, table: Table):
        with self._engine.connect() as conn:
            query_statement = select(table)
            conn.execute(query_statement)

    def create_tables(self,):
        self._metadata.create_all(self._engine)

    def drop_tables(self):
        self._metadata.drop_all(self._engine)
