from pydantic import BaseModel
from typing import Optional


class ModelConfigCreate(BaseModel):
    """模型配置请求"""
    provider: str
    model_name: str
    api_key: str
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000


class ModelConfigResponse(BaseModel):
    """模型配置响应"""
    provider: str
    model_name: str
    base_url: Optional[str] = None
    temperature: float
    max_tokens: int
    is_configured: bool


class TestConnectionRequest(BaseModel):
    """连接测试请求"""
    provider: str
    model_name: str
    api_key: str
    base_url: Optional[str] = None


class TestConnectionResponse(BaseModel):
    """连接测试响应"""
    success: bool
    message: str
    latency_ms: Optional[float] = None
