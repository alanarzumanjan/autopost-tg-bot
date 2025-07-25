from aiogram import types
from aiogram.dispatcher import Dispatcher


async def start_handler(message: types.Message):
    await message.answer("""
        <strong>Hello! I'am Content Manager Bot!</strong>
        I can help you:
                <strong>/start</strong> - start program and send command lists
                <strong>/gen</strong> - generate post for your channel
                <strong>/register_autogen</strong> - register autogeneration posts and public in your telegram channel
                <strong>/contact_with_admin</strong> - you can contact with admin
    """)


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
