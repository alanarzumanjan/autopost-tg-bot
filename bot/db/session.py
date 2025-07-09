from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from bot.config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)