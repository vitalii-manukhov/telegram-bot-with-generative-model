from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import insert, select

from config import settings

class DataBase:
    def __init__(self, db_url):
        self._engine = create_engine(url=settings.url_for_db,
                                     echo=True)
        self._session = sessionmaker(self._engine)
        self._metadata = MetaData(bind=self._engine)

    @classmethod
    def get_table(cls, table_name):
        return Table(table_name, cls._metadata, autoload_with=cls._engine)

    def record_update(self):
        pass

    def record_bot_reply(self):
        pass

    def read_data(self):
        pass

    def create_table(self, table_name):
        pass

    def drop_table(self, table_name):
        pass
