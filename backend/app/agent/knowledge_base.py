"""医学知识库"""
import json
import os
from typing import List, Optional
from app.config import settings


class MedicalKnowledgeBase:
    """医学知识库
    
    提供基础的关键词匹配知识检索
    生产环境建议使用向量数据库（如ChromaDB）实现语义搜索
    """
    
    def __init__(self):
        self.knowledge_dir = settings.KNOWLEDGE_BASE_PATH
        self._knowledge_cache = {}
        self._load_knowledge()
    
    def _load_knowledge(self):
        """加载知识库数据"""
        # 症状知识
        symptoms_file = os.path.join(self.knowledge_dir, "symptoms", "symptom_index.json")
        if os.path.exists(symptoms_file):
            with open(symptoms_file, "r", encoding="utf-8") as f:
                self._knowledge_cache["symptoms"] = json.load(f)
        
        # 疾病知识
        diseases_dir = os.path.join(self.knowledge_dir, "diseases")
        if os.path.exists(diseases_dir):
            self._knowledge_cache["diseases"] = {}
            for filename in os.listdir(diseases_dir):
                if filename.endswith(".json"):
                    filepath = os.path.join(diseases_dir, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        category = filename.replace(".json", "")
                        self._knowledge_cache["diseases"][category] = json.load(f)
    
    def search(self, query: str, top_k: int = 3) -> str:
        """搜索相关医学知识"""
        results = []
        
        # 搜索症状
        symptoms_data = self._knowledge_cache.get("symptoms", {})
        for symptom, info in symptoms_data.items():
            if symptom in query or any(keyword in query for keyword in info.get("keywords", [])):
                results.append(f"【症状】{symptom}: {info.get('description', '')}")
        
        # 搜索疾病
        diseases_data = self._knowledge_cache.get("diseases", {})
        for category, diseases in diseases_data.items():
            for disease in diseases:
                name = disease.get("name", "")
                keywords = disease.get("keywords", [])
                if name in query or any(kw in query for kw in keywords):
                    results.append(f"【{category}】{name}: {disease.get('description', '')}")
        
        # 如果没有找到相关知识，返回通用信息
        if not results:
            return "暂无直接相关的医学知识。建议您详细描述症状，咨询专业医生。"
        
        # 返回前top_k个结果
        return "\n".join(results[:top_k])
    
    def search_by_symptoms(self, symptoms: List[str]) -> str:
        """根据症状列表搜索相关疾病"""
        results = []
        
        diseases_data = self._knowledge_cache.get("diseases", {})
        for category, diseases in diseases_data.items():
            for disease in diseases:
                disease_keywords = disease.get("keywords", [])
                # 检查是否有匹配的症状
                if any(symptom in disease_keywords for symptom in symptoms):
                    results.append({
                        "category": category,
                        "name": disease.get("name", ""),
                        "description": disease.get("description", ""),
                        "department": disease.get("department", "")
                    })
        
        if not results:
            return "未找到直接相关的疾病信息。"
        
        # 格式化输出
        output = []
        for r in results[:5]:
            output.append(f"【{r['category']}】{r['name']}")
            output.append(f"  描述: {r['description']}")
            output.append(f"  就医科室: {r['department']}")
            output.append("")
        
        return "\n".join(output)
    
    def get_common_checkups(self, symptoms: List[str]) -> str:
        """根据症状建议检查项目"""
        # 通用检查建议
        general_checkups = ["血常规", "尿常规", "肝功能", "肾功能"]
        
        symptom_checkup_map = {
            "头痛": ["头颅CT/MRI", "血压测量", "眼底检查"],
            "头晕": ["血常规", "血压测量", "颈椎检查"],
            "恶心": ["胃镜", "肝功能", "腹部B超"],
            "呕吐": ["胃镜", "电解质检查", "腹部B超"],
            "发烧": ["血常规", "C反应蛋白", "胸片"],
            "咳嗽": ["胸片", "血常规", "肺功能检查"],
            "胸闷": ["心电图", "心脏彩超", "胸片"],
            "心悸": ["心电图", "心脏彩超", "甲状腺功能"],
            "腹痛": ["腹部B超", "血常规", "大便常规"],
            "腹泻": ["大便常规", "血常规", "肠镜"],
            "失眠": ["多导睡眠监测", "甲状腺功能"],
            "乏力": ["血常规", "肝功能", "甲状腺功能"],
        }
        
        recommended = []
        for symptom in symptoms:
            if symptom in symptom_checkup_map:
                recommended.extend(symptom_checkup_map[symptom])
        
        # 去重
        recommended = list(set(recommended + general_checkups))
        
        return "、".join(recommended)
