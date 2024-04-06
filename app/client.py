"""..."""
from fastapi import FastAPI, Request
import uvicorn
from aiohttp import ClientSession, ClientResponseError
import requests

from app.logger import Logger
from app.db_helper import db_helper

from utils.config import settings
from utils.models import Update

app = FastAPI()

client_logger = Logger("client_logger")


class Client():
    def get_me(self):
        response = requests.get(settings.url_for_any_method + "getMe")
        print(response.json())

    def run_server(self):
        uvicorn.run("app.client:app",
                    port=settings.UVICORN_PORT,
                    host=settings.UVICORN_HOST,
                    reload=True)

    def stop_server(self):
        pass

    def set_webhook(self):
        response = requests.get(settings.url_for_webhook)
        print(response.json())

    def send_message(self, chat_id: int, data):
        response = requests.post(settings.url_for_send_message,
                                 data=data)
        print(response.json())


@app.post("/")
async def read_root(request: Request):
    db_helper.create_tables()
    client_logger.info("Received POST request to the root")
    update = Update.model_validate(await request.json())
    db_helper.record_update(update)

    from app.telegram_bot import TelegramBot
    data = TelegramBot.process_message(message=update.message)
    db_helper.record_bot_reply(data)

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
