"""..."""
from fastapi import FastAPI, Request
import uvicorn
from config import settings
from models import Update
import requests


class Client():
    def __init__(self, url: str, token: str):
        self._app = FastAPI()
        self._url = url
        self._token = token

    def get_me(self):
        pass

    def start_server(self):
        uvicorn.run("start_fast_api:app",
                    port=settings.UVICORN_PORT,
                    host=settings.UVICORN_HOST,
                    reload=True)

    def stop_server(self):
        pass

    def set_webhook(self):
        response = requests.get(settings.url_for_webhook)

    def send_message(self, chat_id: int, data):
        response = requests.post(settings.url_for_send_message,
                                 data=data)
