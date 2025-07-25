# 🤖 Telegram Бот для Ежедневных Автопостов

**Описание проекта**  
Умный Telegram-бот, который ежедневно публикует автоматически сгенерированные или подобранные посты на интересные и полезные темы в Telegram-канал. Проект сочетает в себе автоматизацию, AI-контент, админ-панель и современный стек технологий.

---

## 🛠 Технологии

### Основной стек:

- **Язык программирования**: Python 🐍
- **Фреймворк для бота**: [aiogram](https://docs.aiogram.dev/en/latest/)
- **Планировщик задач**: [APScheduler](https://apscheduler.readthedocs.io/en/latest/)
- **ORM для базы данных**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **База данных**: PostgreSQL 🐘

### Дополнительные библиотеки:

- `requests` — для работы с HTTP-запросами
- `aiohttp` — асинхронные запросы
- `openai` — генерация текста с помощью GPT

---

## 🖥 Админ-панель

- **Бэкенд**: Flask или FastAPI (ещё в разработке)
- **Фронтенд**: React (панель управления постами, статусом и логами)

---

## ☁️ Хостинг

- **Бэкэнд и бот**: [Render](https://render.com/)
- **Фронтенд (React)**: [Netlify](https://www.netlify.com/) _(возможно)_
- **Контейнеризация**: Docker 🐳

---

## 📅 Функциональность

- [x] Генерация контента через OpenAI
- [x] Публикация в Telegram-канал
- [x] Планировщик на каждый день
- [ ] Админ-панель для ручной модерации
- [ ] Логи и уведомления в случае ошибок

---

## 🚧 Структура проекта (план)

````bash
project/
├── bot/
│   ├── handlers/
│   ├── scheduler/
│   ├── services/
│   └── main.py
├── database/
│   ├── models.py
│   └── db.py
├── admin_panel/ (Flask/FastAPI + React)
├── utils/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
├── .env
└── README.md

## Dependences:

Need to install python 3.11 and click - `Add To System PATH`

👉 [python version 3.11](https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe)

This Version is which works stably with all libraries and dependencies

**Upload dependences:**

```bash
    # check version
    py -3.11 --version

    # Create virtual environment(important)
    py -3.11 -m venv venv
    .\venv\Scripts\activate # (for PowerShell)

    # Start downloading dependences
    pip install -r requirements.txt

```

**Database upgrade:**

```bash
    alembic revision --autogenerate -m "upgrade"
    alembic upgrade head
```

**Database down -1:**

```bash
    alembic downgrade -1
```

````
