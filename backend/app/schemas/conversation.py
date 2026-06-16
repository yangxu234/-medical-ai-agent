from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ConversationCreate(BaseModel):
    """创建对话请求"""
    title: Optional[str] = "新对话"


class ConversationResponse(BaseModel):
    """对话响应"""
    id: int
    title: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
