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
from bot.handlers.gen import register_gen_handler
from bot.db.session import Base, engine
from bot.jobs import setup_scheduler

app = Flask(__name__)

from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

PORT = int(os.environ.get("PORT", 10000))


@app.route("/")
@app.route("/ping")
def ping():
    return "✅ Bot is alive", 200


def run_http():
    logging.info("🚀 Starting HTTP server...")
    app.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

register_start_handler(dp)
register_gen_handler(dp)

if __name__ == "__main__":
    threading.Thread(target=run_http, daemon=True).start()

    async def on_startup():
        logging.info("📦 Initializing DB...")
        Base.metadata.create_all(bind=engine)

        logging.info("🕰️ Launching scheduler...")
        setup_scheduler(bot)

        logging.info("🧹 Cleaning webhook (precaution)...")
        await bot.delete_webhook()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(on_startup())

        logging.info("🤖 Starting bot polling...")
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logging.critical(f"❌ BOT CRASHED: {e}")
