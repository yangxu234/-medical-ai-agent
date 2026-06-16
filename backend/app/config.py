from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    APP_NAME: str = "Medical AI Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./medical_agent.db"
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ENCRYPTION_KEY: str = "your-encryption-key-for-api-keys"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 默认DeepSeek配置
    DEEPSEEK_API_KEY: Optional[str] = None
    DEFAULT_MODEL: str = "deepseek-chat"
    DEFAULT_BASE_URL: str = "https://api.deepseek.com/v1"
    
    # OpenAI配置（可选）
    OPENAI_API_KEY: Optional[str] = None
    
    # 知识库配置
    KNOWLEDGE_BASE_PATH: str = "./knowledge_base"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
