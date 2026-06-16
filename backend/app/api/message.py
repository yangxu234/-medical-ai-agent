"""消息API"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.message import Message
from app.models.conversation import Conversation
from app.schemas.message import MessageCreate, MessageResponse
from app.dependencies import get_current_user
from app.agent.medical_agent import MedicalAgent

router = APIRouter()

# 全局Agent实例
medical_agent = MedicalAgent()


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    data: MessageCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发送消息并获取AI建议（非流式）"""
    
    conversation = db.query(Conversation) \
        .filter(Conversation.id == conversation_id, Conversation.user_id == user_id) \
        .first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")
    
    user_message = Message(conversation_id=conversation_id, role="user", content=data.content)
    db.add(user_message)
    db.commit()
    
    response = await medical_agent.process(
        user_input=data.content, conversation_id=str(conversation_id), user_id=user_id, db=db
    )
    
    ai_message = Message(
        conversation_id=conversation_id, role="assistant",
        content=response["advice"], metadata_json=response.get("metadata", {})
    )
    db.add(ai_message)
    
    if not conversation.title or conversation.title == "新对话":
        conversation.title = data.content[:20] + ("..." if len(data.content) > 20 else "")
    
    db.commit()
    db.refresh(ai_message)
    
    return ai_message


@router.post("/{conversation_id}/messages/stream")
async def send_message_stream(
    conversation_id: int,
    data: MessageCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发送消息并流式获取AI建议（SSE）"""
    
    conversation = db.query(Conversation) \
        .filter(Conversation.id == conversation_id, Conversation.user_id == user_id) \
        .first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")
    
    # 保存用户消息
    user_message = Message(conversation_id=conversation_id, role="user", content=data.content)
    db.add(user_message)
    
    if not conversation.title or conversation.title == "新对话":
        conversation.title = data.content[:20] + ("..." if len(data.content) > 20 else "")
    
    db.commit()
    
    # 流式返回
    async def event_generator():
        full_text = ""
        async for chunk in medical_agent.process_stream(
            user_input=data.content, conversation_id=str(conversation_id), user_id=user_id, db=db
        ):
            full_text += _extract_text_from_sse(chunk)
            yield chunk
        
        # 流结束后保存AI回复到数据库
        from app.database import SessionLocal
        save_db = SessionLocal()
        try:
            ai_message = Message(
                conversation_id=conversation_id, role="assistant",
                content=full_text, metadata_json={"streaming": True}
            )
            save_db.add(ai_message)
            save_db.commit()
        finally:
            save_db.close()
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")


def _extract_text_from_sse(sse_data: str) -> str:
    """从SSE数据中提取文本"""
    import json
    try:
        line = sse_data.strip()
        if line.startswith("data: "):
            payload = json.loads(line[6:])
            if payload.get("type") == "content":
                return payload.get("text", "")
            elif payload.get("type") == "correct":
                return ""  # correct会替换全部内容
    except Exception:
        pass
    return ""


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取对话消息历史"""
    conversation = db.query(Conversation) \
        .filter(Conversation.id == conversation_id, Conversation.user_id == user_id) \
        .first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")
    
    messages = db.query(Message) \
        .filter(Message.conversation_id == conversation_id) \
        .order_by(Message.created_at.asc()) \
        .all()
    
    return messages
