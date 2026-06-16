from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Message(Base):
    """消息表"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user 或 assistant
    content = Column(Text, nullable=False)
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())
    
    # 关联
    conversation = relationship("Conversation", back_populates="messages")
