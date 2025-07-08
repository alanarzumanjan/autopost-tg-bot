from aiogram import types
from aiogram.dispatcher import Dispatcher


async def start_handler(message: types.Message):
    await message.answer("Hello! I am ready to public posts every day!")


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
