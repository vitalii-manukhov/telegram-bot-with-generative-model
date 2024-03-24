from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import Column, Integer, Date, String, MetaData, Table


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

test_table = Table(
    "test",
    metadata_object,
    Column("id", Integer, primary_key=True),
    Column("date", Date),
    Column("number", Integer),
    Column("description", String),
)
