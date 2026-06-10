from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from config.database import Base


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)

    role = Column(String, nullable=False)  # "user" or "assistant"
    sender_id = Column(Integer, nullable=True)  # user only
    sender_name = Column(String, nullable=True) # user or "assistant"

    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

