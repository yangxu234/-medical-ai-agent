"""知识库API"""
from fastapi import APIRouter
from app.agent.knowledge_base import MedicalKnowledgeBase

router = APIRouter()
knowledge_base = MedicalKnowledgeBase()


@router.get("/search")
async def search_knowledge(q: str):
    """搜索医学知识"""
    result = knowledge_base.search(q)
    return {"query": q, "results": result}


@router.get("/symptoms")
async def search_by_symptoms(symptoms: str):
    """根据症状搜索"""
    symptom_list = [s.strip() for s in symptoms.split(",")]
    result = knowledge_base.search_by_symptoms(symptom_list)
    return {"symptoms": symptom_list, "results": result}


@router.get("/checkups")
async def get_checkup_suggestions(symptoms: str):
    """获取检查项目建议"""
    symptom_list = [s.strip() for s in symptoms.split(",")]
    result = knowledge_base.get_common_checkups(symptom_list)
    return {"symptoms": symptom_list, "checkups": result}
