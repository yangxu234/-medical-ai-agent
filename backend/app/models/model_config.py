from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class UserModelConfig(Base):
    """用户模型配置表"""
    __tablename__ = "user_model_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # 提供商配置
    provider = Column(String(50), nullable=False, default="deepseek")
    model_name = Column(String(100), nullable=False, default="deepseek-chat")
    api_key_encrypted = Column(String(500))
    base_url = Column(String(200))
    
    # 模型参数
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=2000)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # 关联
    user = relationship("User", back_populates="model_config")
    
    @classmethod
    def get_by_user(cls, db, user_id: int):
        """获取用户配置"""
        return db.query(cls).filter(cls.user_id == user_id).first()
