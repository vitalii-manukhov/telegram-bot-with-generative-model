from app.base_bot import Bot
from typing import Dict, Any
import torch

from transformers import pipeline
from transformers import FSMTForConditionalGeneration, FSMTTokenizer

from utils.models import Message, KeyboardButton, ReplyKeyboardMarkup
from utils.config import settings

import os
os.environ['HF_HOME'] = settings.HF_CACHE_DIR


class TelegramBot(Bot):
    @staticmethod
    def process_message(message: Message) -> Dict[str, Any]:
        """..."""
        button_text = "Пожелай мне чего-нибудь!"
        keyboard_button = KeyboardButton(text=button_text)

        if message.text == "/start":
            reply_text = f"Здравствуйте, {message.from_user.first_name}!"

            data = {
                "chat_id": message.chat.chat_id,
                "text": reply_text,
                "reply_markup": ReplyKeyboardMarkup(
                    keyboard=[[keyboard_button]]).model_dump_json()
            }

            return data
        elif message.text == "Пожелай мне чего-нибудь!":
            query = "Wish me something!"
            reply = generate_reply(query)
            reply = translate_reply(reply)

            data = {
                "chat_id": message.chat.chat_id,
                "text": reply,
                "reply_markup": ReplyKeyboardMarkup(
                    keyboard=[[keyboard_button]]).model_dump_json()
            }

            return data

        reply_text = "Не могу разобрать ваше сообщение"
        data = {
            "chat_id": message.chat.chat_id,
            "text": reply_text,
            "reply_markup": ReplyKeyboardMarkup(
                keyboard=[[keyboard_button]]).model_dump_json()
        }

        return data


def generate_reply(query: str) -> str:
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    task = "text-generation"
    pipe = pipeline(task=task,
                    model=model_id,
                    torch_dtype=torch.bfloat16,
                    device_map="auto",
                    )
    messages = [
        {
            "role": "system",
            "content": (
                "You're a chatbot that responds in"
                "a very short and friendly manner.")
        },
        {"role": "user", "content": query}
    ]

    prompt = pipe.tokenizer.apply_chat_template(messages,
                                                tokenize=False,
                                                add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=128,
                   do_sample=True,
                   temperature=0.35,
                   top_k=50,
                   top_p=0.95)
    reply = outputs[0]["generated_text"]

    specific_string = "<|assistant|>"
    index = reply.find(specific_string)
    substring = reply[index + len(specific_string):]

    return substring


def translate_reply(text: str) -> str:
    model_id = "facebook/wmt19-en-ru"
    tokenizer = FSMTTokenizer.from_pretrained(model_id)
    model = FSMTForConditionalGeneration.from_pretrained(model_id)

    input_ids = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(input_ids)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
