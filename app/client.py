"""..."""
from fastapi import FastAPI, Request
import uvicorn
from config import settings
from models import Update
import requests
from aiohttp import ClientSession, ClientResponseError
from logger import Logger
from database import DataBase

app = FastAPI()

client_logger = Logger("client_logger")


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
    database = DataBase()
    database.create_tables()
    client_logger.info("Received POST request to the root")
    update = Update.model_validate(await request.json())
    database.record_update(update)

    from telegram_bot import TelegramBot
    data = TelegramBot.process_message(message=update.message)
    database.record_bot_reply(data)

    async with ClientSession() as session:
        async with session.post(settings.url_for_send_message,
                                data=data) as response:
            client_logger.info("Post request sent")
            if response.status != 200:
                raise ClientResponseError(
                    response.request_info,
                    response.history,
                    message="Unexpected status code: {response.status}")

    return {"status_code": 200}
