import logging
import threading
import os
import asyncio

from flask import Flask
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import set_webhook
from werkzeug.middleware.proxy_fix import ProxyFix

from bot.config import BOT_TOKEN
from bot.handlers.start import register_start_handler
from bot.db.session import Base, engine
from bot.jobs import setup_scheduler

PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)


@app.route("/")
@app.route("/ping")
def ping():
    return "✅ Bot is alive", 200


def run_http():
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

register_start_handler(dp)

if __name__ == "__main__":
    logging.info("🚀 Starting HTTP ping server...")
    threading.Thread(target=run_http).start()

    logging.info("📦 Initializing database...")
    Base.metadata.create_all(bind=engine)

    logging.info("🕰️ Launching scheduler...")
    setup_scheduler(bot)

    logging.info("🤖 Bot is starting...")
    asyncio.get_event_loop().run_until_complete(bot.delete_webhook())

    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logging.critical(f"❌ Bot crashed with error: {e}")
