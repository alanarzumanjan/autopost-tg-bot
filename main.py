import logging
from aiogram import Bot, Dispatcher, executor
from bot.config import BOT_TOKEN
from bot.handlers.start import register_start_handler
from bot.db.models import Post
from bot.db.session import Base, engine
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

register_start_handler(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

Base.metadata.create_all(bind=engine)