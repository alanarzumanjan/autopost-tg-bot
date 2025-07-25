from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
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

    post_sends = relationship("PostSend", back_populates="post")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, index=True)  # Telegram ID
    full_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    subscription_level = Column(
        String, default="free"
    )  # free / basic / pro / unlimited
    registration_step = Column(
        String, default=None
    )  # 'awaiting_tariff', 'awaiting_channel', None

    created_at = Column(DateTime, default=datetime.utcnow)

    channels = relationship("UserChannel", back_populates="user")


class UserChannel(Base):
    __tablename__ = "user_channels"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    custom_prompt = Column(Text, nullable=True)
    tg_channel_id = Column(String, unique=True)  # @username or chat_id
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="channels")
    sends = relationship("PostSend", back_populates="channel")


class PostSend(Base):
    __tablename__ = "post_sends"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    channel_id = Column(Integer, ForeignKey("user_channels.id"))
    sent_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="post_sends")
    channel = relationship("UserChannel", back_populates="sends")


class UserGenLimit(Base):
    __tablename__ = "user_gen_limits"

    user_id = Column(Integer, primary_key=True)
    count = Column(Integer, default=0)
    last_reset = Column(DateTime, default=datetime.utcnow)
