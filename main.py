import logging
import asyncio
from aiogram import Bot, Dispatcher, executor
from bot.config import BOT_TOKEN
from bot.handlers.start import register_start_handler
from bot.db.models import Post
from bot.db.session import Base, engine
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.jobs import setup_scheduler
import threading
from flask import Flask
import os

PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)


@app.route("/")
@app.route("/ping")
def ping():
    return "✅ Bot is alive", 200


def run_http():
    app.run(host="0.0.0.0", port=PORT)


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

register_start_handler(dp)


async def main():
    # Создание таблиц в БД
    Base.metadata.create_all(bind=engine)

    # Запуск планировщика
    setup_scheduler(bot)

    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    threading.Thread(target=run_http).start()
    asyncio.run(main())
