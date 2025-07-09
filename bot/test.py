import asyncio
from bot.generator import generate_post

async def main():
    text = await generate_post("технологии")
    print("Сгенерированный пост:\n")
    print(text)

if __name__ == "__main__":
    asyncio.run(main())
