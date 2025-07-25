from .session import SessionLocal
from .models import Post, PostSend
from datetime import datetime, timezone


def get_scheduled_post():
    db = SessionLocal()
    try:
        post = (
            db.query(Post)
            .filter_by(published=False)
            .order_by(Post.scheduled_for.asc())
            .first()
        )
        return post
    finally:
        db.close()


def mark_post_as_published(post_id: int):
    db = SessionLocal()
    try:
        post = db.query(Post).get(post_id)
        if post:
            post.published = True
            db.commit()
    finally:
        db.close()


def add_post(title: str, content: str, scheduled_for=None, is_ai_generated=True):
    db = SessionLocal()
    try:
        if scheduled_for and scheduled_for.tzinfo is None:
            scheduled_for = scheduled_for.replace(tzinfo=timezone.utc)
        elif scheduled_for and scheduled_for.tzinfo:
            scheduled_for = scheduled_for.astimezone(timezone.utc)

        new_post = Post(
            title=title,
            content=content,
            scheduled_for=scheduled_for.replace(tzinfo=None)
            if scheduled_for
            else None,  # в БД хранится без tz
            is_ai_generated=is_ai_generated,
        )

        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    finally:
        db.close()


def was_post_sent(post_id: int, channel_id: int) -> bool:
    db = SessionLocal()
    try:
        return (
            db.query(PostSend).filter_by(post_id=post_id, channel_id=channel_id).first()
            is not None
        )
    finally:
        db.close()


def record_post_send(post_id: int, channel_id: int):
    db = SessionLocal()
    try:
        send = PostSend(
            post_id=post_id, channel_id=channel_id, sent_at=datetime.utcnow()
        )
        db.add(send)
        db.commit()
    finally:
        db.close()
