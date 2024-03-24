"""..."""
from fastapi import FastAPI, Request
import uvicorn
from config import settings
from models import Update, ReplyKeyboardMarkup, KeyboardButton
import requests
from aiohttp import ClientSession, ClientResponseError

app = FastAPI()


class Client():
    def get_me(self):
        response = requests.get(settings.url_for_any_method + "getMe")
        print(response.json())

    def run_server(self):
        uvicorn.run("client:app",
                    port=settings.UVICORN_PORT,
                    host=settings.UVICORN_HOST,
                    reload=True)

    def stop_server(self):
        pass

    def set_webhook(self):
        requests.get(settings.url_for_webhook)

    def send_message(self, chat_id: int, data):
        response = requests.post(settings.url_for_send_message,
                                 data=data)
        print(response.json())


@app.post("/")
async def read_root(request: Request):
    update = Update.model_validate(await request.json())
    # reply = f"Ваше имя: {update.message.from_user.first_name}"

    # data = {
    #     "chat_id": update.message.chat.chat_id,
    #     "text": reply
    # }

    # async with ClientSession() as session:
    #     async with session.post(settings.url_for_send_message,
    #                             data=data) as response:
    #         if response.status != 200:
    #             raise ClientResponseError(
    #                 response.request_info,
    #                 response.history,
    #                 message="Unexpected status code: {response.status}"
    #             )

    button_text = "Пожелай мне чего-нибудь хорошего!"
    message_text = "Нажми на кнопку"
    data = {
        "chat_id": update.message.chat.chat_id,
        "text": message_text,
        "reply_markup": ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=button_text)]]).model_dump_json()
    }

    response = requests.post(
        settings.url_for_send_message,
        data=data
    )

    print(response.json())

    # async with ClientSession() as session:
    #     async with session.post(settings.url_for_any_method +
    #                             "editMessageReplyMarkup",
    #                             data=data) as response:
    #         if response.status != 200:
    #             raise ClientResponseError(
    #                 response.request_info,
    #                 response.history,
    #                 message=f"Unexpected status code: {response.status}"
    #             )
