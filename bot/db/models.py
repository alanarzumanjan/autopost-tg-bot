from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from datetime import datetime
from .session import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    scheduled_for = Column(DateTime, nullable=True)
    published = Column(Boolean, default=False)
    is_ai_generated = Column(Boolean, default=True)