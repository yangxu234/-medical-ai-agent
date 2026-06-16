"""对话API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate, ConversationResponse
from app.dependencies import get_current_user

router = APIRouter()


@router.post("", response_model=ConversationResponse)
async def create_conversation(
    data: ConversationCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新对话"""
    conversation = Conversation(
        user_id=user_id,
        title=data.title or "新对话"
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return conversation


@router.get("", response_model=List[ConversationResponse])
async def get_conversations(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户所有对话"""
    conversations = db.query(Conversation) \
        .filter(Conversation.user_id == user_id) \
        .order_by(Conversation.updated_at.desc()) \
        .all()
    
    return conversations


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取对话详情"""
    conversation = db.query(Conversation) \
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ) \
        .first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")
    
    return conversation


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除对话"""
    conversation = db.query(Conversation) \
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        ) \
        .first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")
    
    # 删除关联的消息
    from app.models.message import Message
    db.query(Message).filter(Message.conversation_id == conversation_id).delete()
    
    db.delete(conversation)
    db.commit()
    
    return {"message": "删除成功"}
