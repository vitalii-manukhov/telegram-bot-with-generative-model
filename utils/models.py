from pydantic import BaseModel, Field
from typing import Optional, List


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

    def full_unpack(self):
        data = {
            "update_id": self.update_id,
            "message_id": self.message.message_id,
            "user_id": self.message.from_user.user_id,
            "is_bot": self.message.from_user.is_bot,
            "first_name": self.message.from_user.first_name,
            "username": self.message.from_user.username,
            "language_code": self.message.from_user.language_code,
            "chat_id": self.message.chat.chat_id,
            "chat_type": self.message.chat.chat_type,
            "date": self.message.date,
            "text": self.message.text
        }

        return data


class KeyboardButton(BaseModel):
    text: str = '_'


class ReplyKeyboardMarkup(BaseModel):
    keyboard: List[List[KeyboardButton]]
