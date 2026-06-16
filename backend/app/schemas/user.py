from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """用户注册请求"""
    email: str
    name: str
    password: str


class UserLogin(BaseModel):
    """用户登录请求"""
    email: str
    password: str


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    email: str
    name: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token响应"""
    access_token: str
    token_type: str = "bearer"
