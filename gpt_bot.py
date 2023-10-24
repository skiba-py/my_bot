import os

import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
openai.api_key = os.getenv('OPEN_AI_TOKEN')

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


@dp.message_handler()
async def send(message: types.Message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.text}
        ]
    )
    await message.answer(response['choices'][0]['message']['content'])

executor.start_polling(dp, skip_updates=True)
