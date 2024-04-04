from pydantic import BaseModel, Field
from typing import Optional, List

from sqlalchemy import Column, MetaData, Table
from sqlalchemy import Integer, Date, String, Boolean


class Chat(BaseModel):
    chat_id: int = Field(alias="id")
    first_name: str
    last_name: Optional[str] = None
    username: str
    chat_type: str = Field(alias="type")


class User(BaseModel):
    user_id: int = Field(alias="id")
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: str
    language_code: str


class Message(BaseModel):
    message_id: int
    from_user: User = Field(alias="from")
    chat: Chat
    date: int
    text: Optional[str] = None
    animation: Optional[str] = None
    audio: Optional[str] = None
    sticker: Optional[str] = None
    video: Optional[str] = None


class Update(BaseModel):
    update_id: int
    message: Message


metadata_object = MetaData()

updates_table = Table(
    "updates",
    metadata_object,
    Column("update_id", Integer, primary_key=True),
    Column("message_id", Integer),
    Column("user_id", Integer),
    Column("is_bot", Boolean),
    Column("first_name", String),
    Column("username", String),
    Column("language_code", String),
    Column("chat_id", Integer),
    Column("chat_type", String),
    Column("date", Date),
    Column("text", String),
)

replies_table = Table(
    "replies",
    metadata_object,
    Column("reply_id", Integer, primary_key=True),
    Column("chat_id", Integer),
    Column("text", String)
)


class KeyboardButton(BaseModel):
    text: str = '_'


class ReplyKeyboardMarkup(BaseModel):
    keyboard: List[List[KeyboardButton]]
