from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Boolean


class Base(DeclarativeBase):
    pass


class Update(Base):
    __tablename__ = "updates"

    update_id: Mapped[int] = mapped_column("update_id",
                                           Integer,
                                           primary_key=True)
    message_id: Mapped[int] = mapped_column("message_id", Integer)
    user_id: Mapped[int] = mapped_column("user_id", Integer)
    is_bot: Mapped[bool] = mapped_column("is_bot", Boolean)
    first_name: Mapped[str] = mapped_column("first_name", String)
    username: Mapped[str] = mapped_column("username", String)
    language_code: Mapped[str] = mapped_column("language_code", String)
    chat_id: Mapped[int] = mapped_column("chat_id", Integer)
    chat_type: Mapped[str] = mapped_column("chat_type", String)
    date: Mapped[int] = mapped_column("date", Integer)
    text: Mapped[str] = mapped_column("text", String)


class BotReply(Base):
    __tablename__ = "replies"

    reply_id: Mapped[int] = mapped_column("reply_id",
                                          Integer,
                                          primary_key=True)
    chat_id: Mapped[int] = mapped_column("chat_id", Integer)
    text: Mapped[str] = mapped_column("text", String)
