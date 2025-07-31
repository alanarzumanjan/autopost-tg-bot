from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.db.session import SessionLocal
from bot.db.models import User
from bot.config import PAYMENT_PROVIDER_TEST

# 💰 Тарифы и цены (в евро * 100)
TARIFFS = {
    "basic": {"title": "Basic", "amount": 299, "desc": "2 поста в день"},
    "pro": {"title": "Pro", "amount": 599, "desc": "5 постов в день"},
    "unlimited": {"title": "Unlimited", "amount": 999, "desc": "Без ограничений"},
}

CURRENCY = "EUR"


async def settariff_handler(message: types.Message):
    args = message.get_args().strip().lower()
    user_id = message.from_user.id

    if not args or args not in TARIFFS:
        text = "<b>💳 Доступные тарифы:</b>\n"
        for key, val in TARIFFS.items():
            text += f"/settariff {key} — {val['title']} ({val['amount'] / 100:.2f}€)\n"
        await message.reply(text, parse_mode="HTML")
        return

    selected = TARIFFS[args]

    prices = [types.LabeledPrice(label=selected["title"], amount=selected["amount"])]

    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title=f"Тариф: {selected['title']}",
        description=selected["desc"],
        payload=f"tariff_{args}",
        provider_token=PAYMENT_PROVIDER_TEST,
        currency=CURRENCY,
        prices=prices,
        start_parameter="settariff-payment",
    )


async def successful_payment_handler(message: types.Message):
    user_id = message.from_user.id
    payload = message.successful_payment.invoice_payload

    if not payload.startswith("tariff_"):
        return

    tariff = payload.split("_")[1]

    db = SessionLocal()
    user = db.query(User).filter_by(tg_id=user_id).first()
    if user:
        user.subscription_level = tariff
        db.commit()
        await message.reply(
            f"✅ Оплата прошла успешно!\nТариф <b>{tariff}</b> активирован.",
            parse_mode="HTML",
        )
    else:
        await message.reply("⚠️ Пользователь не найден в системе.")
    db.close()


def register_settariff_handler(dp: Dispatcher):
    dp.register_message_handler(settariff_handler, commands=["settariff"])
    dp.register_message_handler(
        successful_payment_handler, content_types=types.ContentType.SUCCESSFUL_PAYMENT
    )
