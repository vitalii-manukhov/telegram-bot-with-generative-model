"""..."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import uvicorn
from aiohttp import ClientSession, ClientResponseError
import requests

from app.logger import Logger
from app.db_helper import db_helper

from utils.config import settings
from utils.models import Update
from utils.schemas import BotReply

client_logger = Logger("client_logger")


class Client():
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

    @staticmethod
    def delete_webhook():
        response = requests.get(settings.url_for_delete_webhook)
        print(response)

    def send_message(self, chat_id: int, data):
        response = requests.post(settings.url_for_send_message,
                                 data=data)
        print(response.json())


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper._engine.begin() as conn:
        await conn.run_sync(db_helper._metadata.drop_all)
        await conn.run_sync(db_helper._metadata.create_all)

    yield
    Client.delete_webhook()

app = FastAPI(lifespan=lifespan)


@app.post("/")
async def read_root(request: Request):
    client_logger.info("Received POST request to the root")
    update = Update.model_validate(await request.json())
    await db_helper.record_update(update.full_unpack())

    from app.telegram_bot import TelegramBot
    data = TelegramBot.process_message(message=update.message)
    reply = BotReply(
        chat_id=data["chat_id"],
        text=data["text"]
    )
    await db_helper.record_bot_reply(reply)

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
