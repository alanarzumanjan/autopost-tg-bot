import openai
from random import choice, choices, random
from topic_lists import growth_topics, business_topics, tech_topics, team_topics, tools_topics
from bot.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

all_topic_groups = {
    "growth": growth_topics,
    "business": business_topics,
    "tech": tech_topics,
    "team": team_topics,
    "tools": tools_topics
}

topic_weights = {
    "growth": 0.4,
    "business": 0.25,
    "tech": 0.15,
    "team": 0.1,
    "tools": 0.1
}

def pick_weighted_random_topic():
    group_name = choices(list(topic_weights.keys()), weights=topic_weights.values())[0]
    group = all_topic_groups[group_name]
    return random.choice(group)

async def generate_post(topic: str = None) -> str:
    if topic is None:
        topic = pick_weighted_random_topic()
    
    prompt = f"""
    Ты — Telegram-бот, который публикует короткие и полезные посты на тему "{topic}". 
    Цель поста — дать читателю конкретную интересную/полезную идею, факт, приём или навык, который он может запомнить, обсудить или применить.

    Формат:
    - Начни с цепляющего вопроса или удивительного факта (1 предложение)
    - Раскрой идею с примером (6-10 предложений, по делу)
    - Заверши выводом или призывом к размышлению. Если есть чему научиться,
        то приведи конкретные примеры как что поможет, что советуешь делать/сделать кратко из зачем (1–4 предложения)

    Обязательно:
    - Будь живым и энергичным в стиле, избегай шаблонов и общих слов, живо, без штампов. Можно чуть дерзко, с характером.
    - Приводи конкретику (кейсы, цифры, реальных проектов или эффектов).
    - Используй эмодзи уместно, не перегружай.
    - Обязательно закончить фразой, а не на середине.
    """

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты Telegram-бот для делового канала. Пиши умно, чётко, с пользой."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=600
        )

        content = response.choices[0].message.content.strip()
        tokens = response.usage.total_tokens
        print(f"\n📊 Потрачено токенов: {tokens}")

        with open("generation_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{topic} | {tokens} токенов\n")

        return content
    
    except Exception as e:
        print(f"Ошибка генерации поста: {e}")
        return None
    
