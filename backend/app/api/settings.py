"""配置API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.model_config import UserModelConfig
from app.schemas.model_config import (
    ModelConfigCreate,
    ModelConfigResponse,
    TestConnectionRequest,
    TestConnectionResponse
)
from app.dependencies import get_current_user
from app.agent.llm_factory import LLMFactory
from app.agent.providers import PROVIDER_CONFIG
from app.utils.security import APIKeyManager

router = APIRouter()
llm_factory = LLMFactory()
key_manager = APIKeyManager()


@router.get("/providers")
async def get_providers():
    """获取支持的模型提供商列表"""
    return PROVIDER_CONFIG


@router.get("/model", response_model=ModelConfigResponse)
async def get_my_config(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户当前模型配置"""
    config = db.query(UserModelConfig) \
        .filter(UserModelConfig.user_id == user_id) \
        .first()
    
    if not config:
        # 返回默认配置
        return ModelConfigResponse(
            provider="deepseek",
            model_name="deepseek-chat",
            base_url=None,
            temperature=0.7,
            max_tokens=2000,
            is_configured=False
        )
    
    return ModelConfigResponse(
        provider=config.provider,
        model_name=config.model_name,
        base_url=config.base_url,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        is_configured=bool(config.api_key_encrypted)
    )


@router.post("/model")
async def save_model_config(
    config: ModelConfigCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """保存模型配置"""
    # 加密API Key
    encrypted_key = key_manager.encrypt_key(config.api_key)
    
    # 查找或创建配置
    existing = db.query(UserModelConfig) \
        .filter(UserModelConfig.user_id == user_id) \
        .first()
    
    if existing:
        existing.provider = config.provider
        existing.model_name = config.model_name
        existing.api_key_encrypted = encrypted_key
        existing.base_url = config.base_url
        existing.temperature = config.temperature
        existing.max_tokens = config.max_tokens
    else:
        new_config = UserModelConfig(
            user_id=user_id,
            provider=config.provider,
            model_name=config.model_name,
            api_key_encrypted=encrypted_key,
            base_url=config.base_url,
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        db.add(new_config)
    
    db.commit()
    
    return {"message": "配置保存成功"}


@router.post("/test-connection", response_model=TestConnectionResponse)
async def test_connection(request: TestConnectionRequest):
    """测试模型连接"""
    result = llm_factory.test_connection(
        provider=request.provider,
        model_name=request.model_name,
        api_key=request.api_key,
        base_url=request.base_url
    )
    
    return TestConnectionResponse(**result)


@router.delete("/model")
async def reset_config(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """重置为默认配置"""
    config = db.query(UserModelConfig) \
        .filter(UserModelConfig.user_id == user_id) \
        .first()
    
    if config:
        db.delete(config)
        db.commit()
    
    return {"message": "已重置为默认配置"}
