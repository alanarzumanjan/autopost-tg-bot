import logging
import threading
import os

from flask import Flask
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config import BOT_TOKEN
from bot.handlers.start import register_start_handler
from bot.db.session import Base, engine
from bot.jobs import setup_scheduler

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

if __name__ == "__main__":
    threading.Thread(target=run_http).start()  # HTTP сервер
    Base.metadata.create_all(bind=engine)  # Создание таблиц
    setup_scheduler(bot)  # Планировщик
    executor.start_polling(dp, skip_updates=True)  # Запуск бота
