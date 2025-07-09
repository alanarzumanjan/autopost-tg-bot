from bot.db.session import Base, engine
from bot.db import models

def init():
    print("Table updating...")
    Base.metadata.create_all(bind=engine)
    print("Ready!")

if __name__ == "__main__":
    init()