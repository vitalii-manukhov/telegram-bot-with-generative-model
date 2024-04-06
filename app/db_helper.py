from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from utils.config import settings
from utils.schemas import Update, Base, BotReply

from typing import Any


class DatabaseHelper:
    def __init__(self):
        self._engine = create_async_engine(url=settings.url_for_db,
                                           echo=False)
        self._session = async_sessionmaker(
            self._engine,
            autocommit=False
        )
        self._metadata = Base.metadata

    async def record_update(self, data: dict[str, Any]):
        update = Update(**data)
        async with self._session.begin() as session:
            session.add(update)
            await session.commit()

    async def record_bot_reply(self, reply: BotReply):
        async with self._session.begin() as session:
            session.add(reply)
            await session.commit()

    def create_tables(self,):
        self._metadata.create_all(self._engine)

    def drop_tables(self):
        self._metadata.drop_all(self._engine)


db_helper = DatabaseHelper()
