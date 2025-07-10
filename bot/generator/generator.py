import openai
from bot.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def generate_post(topic: str = "продуктивность") -> str:
    prompt = f"""
        Ты — бот, публикующий полезные посты в Telegram-канале. Напиши короткий и интересный пост (5–7 предложений) на тему "{topic}". 
        Избегай клише, пиши живо и по делу. Добавь эмодзи, если уместно.
        """

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты Telegram-бот контент-менеджер."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ошибка генерации поста: {e}")
        return None
