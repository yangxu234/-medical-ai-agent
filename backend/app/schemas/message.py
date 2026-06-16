from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class MessageCreate(BaseModel):
    """发送消息请求"""
    content: str


class MessageResponse(BaseModel):
    """消息响应"""
    id: int
    role: str
    content: str
    metadata_json: Optional[dict] = {}
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
